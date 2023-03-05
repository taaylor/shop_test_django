from http import HTTPStatus

import stripe
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView

from common.views import CommonMixin
from orders.forms import OrderForm
from orders.models import Order
from products.models import Basket
from store import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(CommonMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за заказ!'

class CanceledTemplateView(CommonMixin, TemplateView):
    template_name = 'orders/canseled.html'

class OrdersListView(CommonMixin, ListView):
    template_name = 'orders/orders.html'
    title = 'Store - Заказы'
    queryset = Order.objects.all()
    ordering = ('-created')

    def get_queryset(self):
        queryset = super(OrdersListView, self).get_queryset()
        return queryset.filter(initiator=self.request.user)
    
class OrderListView(DetailView):
    template_name = 'orders/order.html'
    model = Order
    
    def get_context_data(self, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        context['title'] = f'Store - Заказ #{self.object.id}'
        return context

class OrderCreateView(CommonMixin, CreateView):
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    title = 'Store - Оформление заказа'
    success_url = reverse_lazy('orders:order_create')


    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        try:
            checkout_session = stripe.checkout.Session.create(
            line_items=baskets.srtipe_products(),
            metadata = {'id_order': self.object.id},
            mode='payment',
            success_url = settings.DOMAIN_NAME + reverse('orders:order_success'),
            cancel_url = settings.DOMAIN_NAME + reverse('orders:order_canceled'),
            )
        except Exception as e:
            return str(e)
        
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)


    def form_valid(self, form):
        form.instance.initiator = self.request.user
        return super(OrderCreateView, self).form_valid(form)
    

@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
    # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
    # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
    # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
        event['data']['object']['id'],
        expand=['line_items'],
        )

    line_items = session.line_items
    # Fulfill the purchase...
    fulfill_order(session)

  # Passed signature verification
    return HttpResponse(status=200)

def fulfill_order(session):
    id_order = int(session.metadata.id_order)
    order = Order.objects.get(id=id_order)
    order.update_after_payment()
