import requests
from django.core.management.base import BaseCommand
from product.models import Category, Product, Brand, Store


class Command(BaseCommand):
    def handle(self, *args, **options):
        category_list = self.get_category()
        # print(category_list)
        # Category.objects.filter(name=categories).order_by('id').first()
        for category_dict in category_list:
            products = self.get_products(category_dict)
            for product in products:
                p = self.create_product(product)
                category_names = product.get("categories").lower().split(",")
                for category in category_names:
                    c, created = Category.objects.get_or_create(name=category)
                    p.categories.add(c)
                if product.get("stores"):
                    stores = product.get("stores").lower().split(",")
                    for store in stores:
                        s, created = Store.objects.get_or_create(name=store)
                        p.stores.add(s)

    def get_category(self):
        """response of the request to extract data from API

        Parameters:

        Returns:
            LIST: list of categories
        """
        response = requests.get("https://fr.openfoodfacts.org/categories.json")
        result_category = response.json()
        data_category = result_category.get('tags')
        categories = [data.get('name') for data in data_category
                      if data.get("name")]
        category_name = categories[0:5]
        print(category_name)
        return category_name

    def get_products(self, category):
        """response of the request to extract data from API
            with queries parameters response : product list according to
            the best categories
        Parameters:
            category (STRING): one category
        Returns:
            LIST: list of products
        """
        query = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": category,
            "sort_by": "unique_scans_n",
            "page_size": 50,
            "json": 1}
        response_product = requests.get(
            "https://fr.openfoodfacts.org/cgi/search.pl?", query)
        result_product = response_product.json()
        return result_product["products"]

    def create_product(self, product):
        name = product.get("product_name")
        nutriscore = product.get("nutrition_grades")
        nova = product.get("nova_group")
        url = product.get("url")
        description = product.get("ingredients_text")
        barcode = product.get("code")
        picture = product.get("image_front_url")
        brands = product.get("brands").lower().split(",")
        for brand in brands:
            b, created = Brand.objects.get_or_create(
                name=brand)

        p, created = Product.objects.get_or_create(
            name=name, nutriscore=nutriscore, nova=nova, url=url, barcode=barcode,
            description=description, picture=picture, brand=b)
        return p
