import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from nutella_fans.product.models import Category, Product, Brand, Store
from datetime import datetime


class Command(BaseCommand):

    """
    standalone scripts to call the api and import data to database
    """

    def handle(self, *args, **options):
        """ BaseCommand requires the implementation of handle method
        Called all functions --> call and request of api
                             --> insert into data to database


        Args:
            *args: Description
            **options: Description
        """
        now = datetime.now()
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        self.stdout.write(self.style.WARNING(
            "Début de la mise à jour des données %s ..." % date_time))
        try:
            category_list = self.get_category()
            for category_dict in category_list:
                products = self.get_products(category_dict)
                for product in products:
                    p = self.create_product(product)
                    if not p:
                        continue
                    else:
                        category_names = product.get(
                            "categories").lower().split(",")
                        for category in category_names:
                            c, created = Category.objects.get_or_create(
                                name=category)
                            p.categories.add(c)
                        if product.get("stores"):
                            stores = product.get("stores").lower().split(",")
                            for store in stores:
                                s, created = Store.objects.get_or_create(
                                    name=store)
                                p.stores.add(s)
            self.stdout.write(self.style.SUCCESS("Mise à jour réussie"))
        except DatabaseError:
            self.stderr.write(self.style.ERROR(
                "La mise à jour a échoué ... "))
        self.stdout.write(self.style.WARNING(
            "Fin de la mise à jour des données %s " %date_time))

    def get_category(self):
        """response of the request to extract data from API

        Returns:
            LIST: list of categories
        """
        self.stdout.write(self.style.WARNING(
            "Appel à l'api et récupération des 10 meilleurs catégories"))
        response = requests.get("https://fr.openfoodfacts.org/categories.json")
        result_category = response.json()
        data_category = result_category.get('tags')
        categories = [data.get('name') for data in data_category
                      if data.get("name")]
        category_name = categories[0:10]
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
        self.stdout.write(self.style.WARNING(
            "Récupération des données openfoodfacts --> produits"))
        query = {
            "action": "process",
            "tagtype_0": "categories",
            "tag_contains_0": "contains",
            "tag_0": category,
            "sort_by": "unique_scans_n",
            "page_size": settings.MAX_IMPORT_PRODUCTS,
            "json": 1}
        response_product = requests.get(
            "https://fr.openfoodfacts.org/cgi/search.pl?", query)
        result_product = response_product.json()
        return result_product["products"]

    def create_product(self, product):
        """Creation of product on product_product table
            Get product_name or barcode from api for example and
            insert into on Model Product and others Model thanks to relationship

        Args:
            product (INT): one product

        Returns:
            Dict: one product information request to insert on database
        """
        if (product.get('product_name') and product.get('nutrition_grades')):
            name = product.get("product_name")
            nutriscore = product.get("nutrition_grades")
            nova = product.get("nova_group")
            url = product.get("url")
            description = product.get("ingredients_text")
            barcode = product.get("code")
            picture = product.get("image_front_url")
            fat_100g = product.get("nutriments", {}).get("fat_100g")
            fat_level = product.get("nutrient_levels", {}).get("fat")
            salt_100g = product.get("nutriments", {}).get("salt_100g")
            salt_level = product.get("nutrient_levels", {}).get("salt")
            saturated_fat_100g = product.get(
                "nutriments", {}).get("saturated-fat_100g")
            saturated_fat_level = product.get(
                "nutrient_levels", {}).get("saturated-fat")
            sugars_100g = product.get("nutriments", {}).get("sugars_100g")
            sugars_level = product.get("nutrient_levels", {}).get("sugars")
            brands = product.get("brands").lower().split(",")

            b, created = Brand.objects.get_or_create(
                name=brands[0])
            p, created = Product.objects.get_or_create(barcode=barcode, defaults={
                'name': name, 'nutriscore': nutriscore, 'nova': nova, 'url': url, 'description': description, 'picture': picture, 'fat_100g': fat_100g, 'fat_level': fat_level,
                'salt_100g': salt_100g, 'salt_level': salt_level, 'saturated_fat_100g': saturated_fat_100g,
                'saturated_fat_level': saturated_fat_level, 'sugars_100g': sugars_100g, 'sugars_level': sugars_level,
                'brand': b})

            return p
