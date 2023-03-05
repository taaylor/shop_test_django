from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from common.views import CommonMixin
from products.models import *
from users.models import User

# Create your views here.


class IndexView(CommonMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'

class ProductsListView(CommonMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 6
    title = 'Store - Каталог'

    def get_queryset(self):
        prod = cache.get('prod')
        if prod is None:
            queryset = super(ProductsListView, self).get_queryset()
            cache.set('prod', queryset, 3000)
        else:
            queryset = prod
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductsListView, self).get_context_data()
        categories = cache.get('categories')
        if categories is None:
            context['categories'] = ProductCategory.objects.all()
            cache.set('categories', context['categories'], 600)
        else:
            context['categories'] = categories
        return context

@login_required
def basket__add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER']) #возвращает на стр где было выполнено действие


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def basket_remove_all(request):
    basket = Basket.objects.all()
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])      

@login_required 
def minus(request, product_id):
    baskets = Basket.objects.filter(user=request.user, product=Product.objects.get(id=product_id))
   
    if baskets.exists():
        basket = baskets.first()   
        if basket.quantity > 1:   
            basket.quantity -= 1
            basket.save()       
        else:
            baskets.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

@login_required
def plus(request, product_id):
    baskets = Basket.objects.filter(user=request.user, product=Product.objects.get(id=product_id))
   
    if baskets.exists():
        basket = baskets.first()   
        basket.quantity += 1
        basket.save()       
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
