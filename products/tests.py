from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from products.models import Product, ProductCategory
from users.models import User


class IndexViewTestCase(TestCase):

    def test_view(self):
        path = reverse('index') # http://localhost:8000
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        self.assertTemplateUsed(response, 'products/index.html')


class ProductsListViewTestCase(TestCase):
    fixtures = ['categories.json', 'goods.json'] # подгружаем фикстуры

    def setUp(self) -> None: #объявление перемен
        self.products = Product.objects.all()

    def test_list(self):
        path = reverse('products:index')
        response = self.client.get(path)

        self._comon_tests(response)

        self.assertEqual(list(response.context_data['object_list']), list(self.products[:6]))


    def test_list_with_category(self):
        category = ProductCategory.objects.all()
        for cat in category:
            path = reverse('products:category', kwargs={'category_id': cat.id})
            response = self.client.get(path)

            self._comon_tests(response)

            self.assertEqual(
                list(response.context_data['object_list']),
                list(self.products.filter(category_id=cat.id))
            )

    def _comon_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')