# from django.urls import reverse
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from nutella_fans.product.views import ProductListView, ProductDetailView
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
        self.product_id = self.product.pk
        c = Category.objects.create(
            name='aliments et boissons à base de végétaux')
        self.product_search = Product.objects.get(pk=self.product_id)
        self.product.categories.add(c)
        self.client = Client()
        self.product_url = reverse('product_list')
        self.substitute_url = reverse('substitute_list', kwargs={
            'product_id': self.product_id})
        self.factory = RequestFactory()
        return super().setUp()

class ProductListTest(BaseTest):

    def test_get_queryset(self):
        request = self.factory.get(self.product_url)
        view = ProductListView()
        view.request = request

        qs = view.get_queryset()

        self.assertQuerysetEqual(qs, Product.objects.all())

    def test_status_code(self):
        response = self.client.get(self.product_url)
        self.assertEquals(response.status_code, 200)


class SubstituteListTest(TestCase):

    def test_same_category(self):
        brand_p1 = Brand.objects.create(name='ferrero').pk
        brand_p2 = Brand.objects.create(name='Funky Veggie').pk
        brand_p3 = Brand.objects.create(name='La Vache qui rit').pk
        category = Category.objects.create(name='Produits à tartiner')
        other_category = Category.objects.create(name='Produits laitiers')
        product = Product.objects.create(name='Nutella - Ferrero - 400 g',
                                              nutriscore='e', nova=4,
                                              url='https://fr.openfoodfacts.org/produit/'
                                              '3017620422003/nutella-ferrero',
                                              barcode=3017620422003,
                                              description="Sucre, huile de palme, noisettes 13%"
                                              " lait écrémé en poudre 8,7%"
                                              "cacao maigre 7,4%, émulsifiants: lécithines [soja] ; vanilline. Sans gluten",
                                              picture='https://images.openfoodfacts.org/images/'
                                              ' products/301/762/042/2003/front_en.288.400.jpg',
                                              brand_id=brand_p1)
        product_same_category = Product.objects.create(name='OUF! La pâte à tartiner Cacao Noisettes - Funky Veggie - 200 g',
                                                       nutriscore='b', nova=3,
                                                       url='https://fr.openfoodfacts.org/produit/'
                                                       '3770008009653/ouf-la-pate-a-tartiner-cacao-noisettes-funky-veggie',
                                                       barcode=3770008009653,
                                                       description="Purée de haricots rouges* 30% (eau, farine de haricots rouges*),"
                                                       "sucre de fleur de coco*,"
                                                       "eau, purée de noisettes torréfiées* 17,5%, poudre de cacao 4,8%."
                                                       "ingrédients issus de l'agriculture biologique",
                                                       picture='https://images.openfoodfacts.org/images/'
                                                       ' products/377/000/800/9653/front_fr.63.400.jpg',
                                                       brand_id=brand_p2)
        product_other_category = Product.objects.create(name='La Vache qui rit 32 portions - 535 g',
                                                        nutriscore='d', nova=4,
                                                        url='https://fr.openfoodfacts.org/produit/'
                                                        '3073781070309/la-vache-qui-rit-32-portions',
                                                        barcode=3073781070309,
                                                        description="LAIT écrémé réhydraté (origine : France),"
                                                        "FROMAGES, BEURRE, protéines de LAIT,"
                                                        "concentré des minéraux du LAIT,"
                                                        "sels de fonte : polyphosphates, concentré LACTIQUE LAITIER.",
                                                        picture='https://images.openfoodfacts.org/images/'
                                                        ' products/307/378/107/0309/front_fr.64.400.jpg',
                                                        brand_id=brand_p3)
        product.categories.add(category)
        product_same_category.categories.add(category)
        product_other_category.categories.add(other_category)

        response = product.get_substitutes()
        assert product_same_category in response
        assert product_other_category not in response

        def test_same_category_better_nutriscore(self):
            brand_p1 = Brand.objects.create(name='ferrero').pk
            brand_p2 = Brand.objects.create(name='Funky Veggie').pk
            brand_p3 = Brand.objects.create(name='La Vache qui rit').pk
            category = Category.objects.create(name='Produits à tartiner')
            other_category = Category.objects.create(name='Produits laitiers')
            product = Product.objects.create(name='Nutella - Ferrero - 400 g',
                                                  nutriscore='e', nova=4,
                                                  url='https://fr.openfoodfacts.org/produit/'
                                                  '3017620422003/nutella-ferrero',
                                                  barcode=3017620422003,
                                                  description="Sucre, huile de palme, noisettes 13%"
                                                  " lait écrémé en poudre 8,7%"
                                                  "cacao maigre 7,4%, émulsifiants: lécithines [soja] ; vanilline. Sans gluten",
                                                  picture='https://images.openfoodfacts.org/images/'
                                                  ' products/301/762/042/2003/front_en.288.400.jpg',
                                                  brand_id=brand_p1)
            product_better = Product.objects.create(name='OUF! La pâte à tartiner Cacao Noisettes - Funky Veggie - 200 g',
                                                    nutriscore='b', nova=3,
                                                    url='https://fr.openfoodfacts.org/produit/'
                                                    '3770008009653/ouf-la-pate-a-tartiner-cacao-noisettes-funky-veggie',
                                                    barcode=3770008009653,
                                                    description="Purée de haricots rouges* 30% (eau, farine de haricots rouges*),"
                                                    "sucre de fleur de coco*,"
                                                    "eau, purée de noisettes torréfiées* 17,5%, poudre de cacao 4,8%."
                                                    "ingrédients issus de l'agriculture biologique",
                                                    picture='https://images.openfoodfacts.org/images/'
                                                    ' products/377/000/800/9653/front_fr.63.400.jpg',
                                                    brand_id=brand_p2)
            product_worst = Product.objects.create(name='La Vache qui rit 32 portions - 535 g',
                                                   nutriscore='d', nova=4,
                                                   url='https://fr.openfoodfacts.org/produit/'
                                                   '3073781070309/la-vache-qui-rit-32-portions',
                                                   barcode=3073781070309,
                                                   description="LAIT écrémé réhydraté (origine : France),"
                                                   "FROMAGES, BEURRE, protéines de LAIT,"
                                                   "concentré des minéraux du LAIT,"
                                                   "sels de fonte : polyphosphates, concentré LACTIQUE LAITIER.",
                                                   picture='https://images.openfoodfacts.org/images/'
                                                   ' products/307/378/107/0309/front_fr.64.400.jpg',
                                                   brand_id=brand_p3)
            product.categories.add(category)
            product_same_category.categories.add(category)
            product_other_category.categories.add(other_category)
            response = product.get_substitutes()
            assert product_better in response
            assert product_worst not in response

    def test_status_code_200(self):
        brand_p1 = Brand.objects.create(name='ferrero').pk
        product = Product.objects.create(name='Nutella - Ferrero - 400 g',
                                         nutriscore='e', nova=4,
                                         url='https://fr.openfoodfacts.org/produit/'
                                         '3017620422003/nutella-ferrero',
                                         barcode=3017620422003,
                                         description="Sucre, huile de palme, noisettes 13%"
                                         " lait écrémé en poudre 8,7%"
                                         "cacao maigre 7,4%, émulsifiants: lécithines [soja] ; vanilline. Sans gluten",
                                         picture='https://images.openfoodfacts.org/images/'
                                         ' products/301/762/042/2003/front_en.288.400.jpg',
                                         brand_id=brand_p1)
        product_id = product.pk
        substitute_url = reverse('substitute_list', kwargs={
            'product_id': product_id})
        response = self.client.get(substitute_url)
        self.assertEquals(response.status_code, 200)


class ProductDetailTest(TestCase):
    def test_status_code_200(self):
        brand_p2 = Brand.objects.create(name='Funky Veggie').pk
        product_better = Product.objects.create(name='OUF! La pâte à tartiner Cacao Noisettes - Funky Veggie - 200 g',
                                                nutriscore='b', nova=3,
                                                url='https://fr.openfoodfacts.org/produit/'
                                                '3770008009653/ouf-la-pate-a-tartiner-cacao-noisettes-funky-veggie',
                                                barcode=3770008009653,
                                                description="Purée de haricots rouges* 30% (eau, farine de haricots rouges*),"
                                                "sucre de fleur de coco*,"
                                                "eau, purée de noisettes torréfiées* 17,5%, poudre de cacao 4,8%."
                                                "ingrédients issus de l'agriculture biologique",
                                                picture='https://images.openfoodfacts.org/images/'
                                                ' products/377/000/800/9653/front_fr.63.400.jpg',
                                                brand_id=brand_p2)
        detail_id = product_better.pk
        detail_url = reverse('detail_substitute', kwargs={
                             'substitute_id': detail_id})
        response = self.client.get(detail_url)
        assert response.status_code == 200
        self.assertTemplateUsed(response, 'product/detail_substitute.html')

    def test_detail_product(self):
        brand_p2 = Brand.objects.create(name='bjorg').pk
        product_better = Product.objects.create(name='Muesli Raisin, Figue, Abricot',
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
                                                brand_id=brand_p2)
        detail_id = product_better.pk
        # detail_id = product_better.pk
        # detail_url = reverse('detail_substitute', kwargs={
        #                    'substitute_id': detail_id})
        response = product_better.get()
        assert product_better in response
