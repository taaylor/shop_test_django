from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import include, path

from orders.views import (CanceledTemplateView, OrderCreateView, OrderListView,
                          OrdersListView, SuccessTemplateView)

app_name = 'orders'

urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order_create'),
    path('success-order/', SuccessTemplateView.as_view(), name='order_success'),
    path('canceled-order/', CanceledTemplateView.as_view(), name='order_canceled'),
    path('', OrdersListView.as_view(), name='orders_list'),
    path('order/<int:pk>/', OrderListView.as_view(), name='order'),
]