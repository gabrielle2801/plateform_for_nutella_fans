from django.db import models


class Brand(models.Model):

    """Model of the "product_brand" table in the database

    Attributes:
        name (STR): name of brand
    """

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Category(models.Model):

    """Model of the "product_category" table in the database

    Attributes:
        name (STR): name of category imported by OFF API
    """

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Store(models.Model):

    """Model of the "product_store" table in the database

    Attributes:
        name (STR): name of store
    """

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):

    """Model of the "product_product" table in the database
        Relationships --> one to many for Brand
                      --> many to many for Category and Store

    Attributes:
        barcode (STR): Barcode of product
        brand (INT): Foreign key of brand associated
        categories (INT): product_product_categories table ManyToManyField
        description (STR): Description of the product
        fat_100g (INT): Description
        fat_level (STR): Description
        name (STR): name of product
        nova (INT): food processing (1 to 4)
        nutriscore (STR): nutritional quality of food products (A to E)
        picture (STR): url of the product's picture
        salt_100g (TYPE): Description
        salt_level (TYPE): Description
        saturated_fat_100g (TYPE): Description
        saturated_fat_level (TYPE): Description
        stores (TYPE): Description
        sugars_100g (TYPE): Description
        sugars_level (TYPE): Description
        url (TYPE): url of product in OFF web site
    """

    name = models.CharField(max_length=255)
    nutriscore = models.CharField(max_length=1, null=True)
    nova = models.IntegerField(null=True)
    url = models.URLField(max_length=255)
    barcode = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True)
    picture = models.URLField(null=True)
    fat_100g = models.FloatField(null=True)
    fat_level = models.CharField(
        max_length=50, null=True)
    salt_100g = models.FloatField(null=True)
    salt_level = models.CharField(
        max_length=50, null=True)
    saturated_fat_100g = models.FloatField(null=True)
    saturated_fat_level = models.CharField(
        max_length=50, null=True)
    sugars_100g = models.FloatField(null=True)
    sugars_level = models.CharField(
        max_length=50, null=True)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    stores = models.ManyToManyField(Store)

    def get_substitutes(self):
        """ query to list the best products by nutriscore

        Returns:
            List: List of better product by nustriscore
        """
        product_categories = self.categories.all()
        result = Product.objects.filter(categories__in=product_categories)\
            .filter(nutriscore__lt=self.nutriscore)\
            .exclude(pk=self.pk)\
            .order_by('nutriscore').distinct()
        return result
