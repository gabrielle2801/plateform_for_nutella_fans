from django.test import TestCase
from product.models import Product, Category, Brand, Store
from unittest import mock
import requests
from product.management.commands.import_off import Command


class ProductTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Brand.objects.create(name='bjorg')
        Product.objects.create(name='Muesli Raisin, Figue, Abricot',
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
        Category.objects.create(name='aliments et boissons à base de végétaux')

    def test_name_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_name_max_length(self):
        brand = Brand.objects.get(id=1)
        max_length = brand._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

    def test_object_name_is_name(self):
        brand = Brand.objects.get(id=1)
        expected_object_name = brand.name
        self.assertEquals(expected_object_name, str(brand))

    def test_lower_item(self):
        self.assertEquals('BJORG'.lower(), 'bjorg')


class GetCategory(TestCase):

    @mock.patch('requests.get')
    def test_get_categories(self, mock_get):
        mock_response = mock.Mock()
        mock_api = {
            'tags': [{
                'id': 'en:plant-based-foods-and-beverages',
                'known': 1,
                'name': 'Aliments et boissons à base de végétaux',
                'products': 107490,
                'url': 'https://fr.openfoodfacts…ssons-a-base-de-vegetaux'
            }
            ]
        }

        mock_response.json.return_value = mock_api
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = Command().get_category()
        self.assertEquals(result,
                          ["Aliments et boissons à base de végétaux"]
                          )


class GetProduct(TestCase):
    @mock.patch('requests.get')
    def test_get_product(self, mock_get):
        mock_response = mock.Mock()
        expected_json = {

            'products': [{'_id': '3229820129488',
                          'brands': 'Bjork',
                          'categories': "Aliments et boissons à base de végétaux,"
                          " Aliments d'origine végétale, Céréales et pommes de terre,"
                          " Petit-déjeuners, Céréales et dérivés, Céréales pour petit-déjeuner,"
                          " Céréales aux fruits, Mueslis, Mueslis aux fruits",
                          'code': 3229820129488,
                          'url': 'https://fr.openfoodfacts…isin-figue-abricot-bjorg'
                          }
                         ]
        }
        mock_response.json.return_value = expected_json
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        command = Command()
        result = command.get_products(
            "Aliments et boissons à base de végétaux")
        self.assertEquals(result, expected_json["products"])
