from django.urls import path

from products.views import *

app_name = 'products'

urlpatterns = [
    path('', products, name='index'),
    path('category/<int:category_id>/', products, name='category'),
    path('page/<int:page_num>/', products, name='paginator'),
    path('baskets/add/<int:product_id>/', basket__add, name='basket__add'),
    path('baskets/remove/<int:basket_id>/', basket_remove, name='basket_remove'),
    path('baskets/remove_all/', basket_remove_all, name='basket_remove_all'),
    path('baskets/minus/<int:product_id>/', minus, name='minus'),
    path('baskets/plus/<int:product_id>/', plus, name='plus'),
]
