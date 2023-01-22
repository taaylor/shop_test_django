from django.shortcuts import render
from products.models import *
# Create your views here.
def index(request):
    context = {
        'title' : 'Store', 
        'username': 'maksim',
    }
    return render(request, 'products/index.html', context)


def products(request):
    context = {
        'title' : 'Store - Каталог',
        'products': Product.objects.all(),
        'categories': ProductCategory.objects.all(),     
    }
    return render(request, 'products/products.html', context)