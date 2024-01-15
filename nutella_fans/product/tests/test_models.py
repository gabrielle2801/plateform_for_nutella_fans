from django.test import TestCase
from nutella_fans.product.models import Product, Category, Brand, Store
from unittest import mock
# import requests
from nutella_fans.product.management.commands.import_off import Command


class ProductTestCase(TestCase):

    def setUp(self):
        self.brand = Brand.objects.create(name='bjorg').pk
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
                                              brand_id=self.brand
                                              )
        self.product_id = self.product.pk
        self.category = Category.objects.create(
            name='aliments et boissons à base de végétaux').pk
        self.store = Store.objects.create(name='géant casino').pk
        return super().setUp()

    def test_name_label(self):
        product = Product.objects.get(id=self.product_id)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_name_max_length(self):
        brand = Brand.objects.get(id=self.brand)
        max_length = brand._meta.get_field('name').max_length
        self.assertEquals(max_length, 200)

    def test_brand_name_is_name(self):
        brand = Brand.objects.get(id=self.brand)
        expected_object_name = brand.name
        self.assertEquals(expected_object_name, str(brand))

    def test_category_name_is_name(self):
        category = Category.objects.get(id=self.category)
        expected_object_name = category.name
        self.assertEquals(expected_object_name, str(category))

    def test_store_name_is_name(self):
        store = Store.objects.get(id=self.store)
        expected_object_name = store.name
        self.assertEquals(expected_object_name, str(store))

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
                          'url': 'https://fr.openfoodfacts…isin-figue-abricot-bjorg',
                          'nutrient_levels': {'fat': 'moderate', 'salt': 'low', 'saturated-fat': 'low', 'sugars': 'high'},
                          'nutriments': {'fat_100g': 6.3, 'saturated-fat_100g': 1, 'salt_100g': 0.03, 'sugars_100g': 13}
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


class CreateProduct(TestCase):

    def test_not_create_product(self):
        extract_data = {'_id': ' 3017760290692',
                        'product_name': 'Napolitain',
                        'brands': 'Lu',
                        'categories': " Snacks,"
                        " Desserts,"
                        "Snacks sucrés,"
                        "  Biscuits et gâteaux",
                        'code': 3017760290692,
                        'url': 'https://fr.openfoodfacts.org/produit/3017760290692/napolitain-l-original-lu'
                        }
        fat = extract_data.get("nutriments", {}).get("fat_100g")
        print(fat)
        command = Command()
        result = command.create_product(extract_data)
        self.assertFalse(result)

    def test_create_product(self):

        extract_product = {'_id': '3274080005003',
                           'product_name': 'eau',
                           'brands': 'Cristaline',
                           'nutrition_grades': 'a',
                           'categories': " Boissons,"
                           " Eaux, Eaux de sources"
                           " Eaux minérales,"
                           "Eaux minérales naturelles",
                           'code': 3274080005003,
                           'url': 'https://fr.openfoodfacts.org/produit/3274080005003/cristaline-eau-de-source',
                           'nutrient_levels': {'fat': 'low', 'salt': 'low', 'saturated-fat': 'low', 'sugars': 'low'},
                           'nutriments': {'fat_100g': 20, 'saturated-fat_100g': 0, 'salt_100g': 0, 'sugars_100g': 0}
                           }

        command = Command()
        result = command.create_product(extract_product)
        self.assertTrue(result)
        self.assertEquals(result.name, 'eau')

    def test_without_product_name(self):

        extract_product = {'_id': '3274080005003',
                           'brands': 'Cristaline',
                           'nutrition_grades': 'a',
                           'categories': " Boissons,"
                           " Eaux, Eaux de sources"
                           " Eaux minérales,"
                           "Eaux minérales naturelles",
                           'code': 3274080005003,
                           'url': 'https://fr.openfoodfacts.org/produit/3274080005003/cristaline-eau-de-source',
                           'nutrient_levels': {'fat': 'low', 'salt': 'low', 'saturated-fat': 'low', 'sugars': 'low'},
                           'nutriments': {'fat_100g': 20, 'saturated-fat_100g': 0, 'salt_100g': 0, 'sugars_100g': 0}
                           }
        command = Command()
        result = command.create_product(extract_product)
        self.assertFalse(result)
