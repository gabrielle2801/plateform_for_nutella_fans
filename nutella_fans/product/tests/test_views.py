# from django.urls import reverse
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse

from nutella_fans.product.views import ProductListView, SubstituteListView
from nutella_fans.product.models import Product, Brand, Category


class BaseTest(TestCase):
    @classmethod
    def setUp(cls):
        Brand.objects.create(name='bjorg').pk
        Brand.objects.create(name='nutella-b-ready').pk
        product_1 = Product.objects.create(name='Muesli Raisin, Figue, Abricot',
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
                                                brand_id=1
                                           )
        product1_id = product_1.pk
        product_2 = Product.objects.create(name='NUTELLA B-READY biscuits 220g paquet de 10 pièces',
                                                nutriscore='e', nova=4,
                                                url='https://fr.openfoodfacts.org/produit/'
                                                '8000500217078/nutella-b-ready-biscuits-220g-paquet-de-10-pieces-ferrero',
                                                barcode=8000500217078,
                                                description="Pâte à tartiner aux noisettes et au cacao 81,5 %"
                                                " (sucre, huile de palme, noisettes 13%,"
                                                " lait écrémé en poudre 8,7%,cacao maigre 7,4%,"
                                                " levure de bière, extrait de malt d'orge, sel, lait écrémé en poudre,"
                                                " émulsifiants : lécithines [soja] ; protéines de froment, protéines de lait, eau.",
                                                picture='https://images.openfoodfacts.org/images/'
                                                'products/800/050/021/7078/front_fr.63.400.jpg',
                                                brand_id=173

                                           )
        product2_id = product_2.pk
        product_search = Product.objects.get(pk=product1_id)
        product_substitute = Product.objects.get(pk=product2_id)
        category_1 = Category.objects.create(
            name='aliments et boissons à base de végétaux')
        category_2 = Category.objects.create(
            name='snacks sucrés')
        product_1.categories.add(Product.objects.get(pk=product1_id))
        product_2.categories.add(Product.objects.get(pk=product2_id))
        client = Client()
        product_url = reverse('product_list')
        product_id = self.product_1
        substitute_url = reverse(
            'substitute_list', args=[product_id])
        factory = RequestFactory
        return super().setUp()

    class ProductListTest(BaseTest):

        def test_get_queryset(self):
            request = RequestFactory().get(self.product_url)
            view = ProductListView()
            view.request = request

            qs = view.get_queryset()

            self.assertQuerysetEqual(qs, Product.objects.all())

        def test_status_code(self):
            response = self.client.get(self.product_url)
            self.assertEquals(response.status_code, 200)


class SubstituteListTest(BaseTest):

    def test_product_list(self):
        response = self.client.get(self.substitute_url)

        self.assertEquals(response.status_code, 200)
