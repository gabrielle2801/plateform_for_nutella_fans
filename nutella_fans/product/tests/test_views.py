# from django.urls import reverse
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse

from nutella_fans.product.views import ProductListView, SubstituteListView
from nutella_fans.product.models import Product, Brand, Category


class BaseTest(TestCase):

    def setUp(self):
        self.brand_id = Brand.objects.create(name='bjorg').pk
        self.product = Product.objects.create(name='Muesli Raisin, Figue, Abricot',
                                              nutriscore='a', nova=1,
                                              url='https://fr.openfoodfacts.org/produit/'
                                              '3229820129488/muesli-raisin-figue-abricot-bjorg',
                                              barcode=3229820129488,
                                              description="Flocons d'avoine* 44%, flocons d'épeautre*"
                                              "(blé) 15%, raisins* 10%, (raisins*, huile de tounesol*)"
                                              ", pétales de maïs*, figues* 9% (farine de riz*),"
                                              "graines* 6% (graines de tournesol*,"
                                              "graines de lin*, graines de courge*),"
                                              "abricots* 4% (farine de riz*),"
                                              "pétales d'épeautre* complet (blé) 3%."
                                              "Peut contenir des traces de fruits à coque,"
                                              "lait, graines de sésame, soja et sulfites.",
                                              picture='https://static.openfoodfacts.org/images/'
                                              'products/322/982/012/9488/front_fr.166.400.jpg',
                                              brand_id=self.brand_id
                                              )
        # p = self.create_product(self.product)
        self.product_id = self.product.pk
        c = Category.objects.create(
            name='aliments et boissons à base de végétaux')
        self.product_search = Product.objects.get(pk=self.product_id)
        self.product.categories.add(c)

        self.client = Client()
        self.product_url = reverse('product_list')
        self.product_id = 1
        self.substitute_url = reverse('substitute_list', kwargs={
            'product_id': self.product_id})
        self.factory = RequestFactory()
        return super().setUp()

class ProductListTest(BaseTest):

    def test_get_queryset(self):
        # view.kwargs = dict(pk=self.product_id)
        request = self.factory.get(self.product_url)
        view = ProductListView()
        view.request = request

        qs = view.get_queryset()

        self.assertQuerysetEqual(qs, Product.objects.all())

    def test_status_code(self):
        response = self.client.get(self.product_url)
        self.assertEquals(response.status_code, 200)


class SubstituteListTest(BaseTest):

    def test_get_queryset(self):
        request = self.factory.get(self.substitute_url)
        view = SubstituteListView()
        view.request = request

        kwargs = {'product_id': 2}
        product_categories = self.product.categories.all()
        qs = view.get_queryset(kwargs)

        self.assertQuerysetEqual(
            qs, Product.objects.filter(categories__in=product_categories)
            .filter(nutriscore__lt=self.product.nutriscore)
            .order_by('nutriscore').distinct())

    # def get_queryset(self):
