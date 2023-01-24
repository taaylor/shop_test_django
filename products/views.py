from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from products.models import *
from users.models import User
# Create your views here.
def index(request):
    context = {
        'title' : 'Store', 
        'username': 'maksim',
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None, page_num=1):
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    per_page = 3
    paginator = Paginator(products, per_page)
    prod_paginator = paginator.page(page_num)

    context = {
        'title' : 'Store - Каталог',
        'categories': ProductCategory.objects.all(),
        'products': prod_paginator,     
    }
    return render(request, 'products/products.html', context)

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