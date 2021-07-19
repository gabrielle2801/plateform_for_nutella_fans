# from django.urls import reverse
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse

from product.views import ProductListView
from product.models import Product


class ProductListTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.list = reverse('product_list')

    def test_get_queryset(self):
        request = RequestFactory().get('/product_list')
        view = ProductListView()
        view.request = request

        qs = view.get_queryset()

        self.assertQuerysetEqual(qs, Product.objects.all())

    def test_status_code_302(self):
        response = self.client.get(self.list)
        self.assertEquals(response.status_code, 200)
