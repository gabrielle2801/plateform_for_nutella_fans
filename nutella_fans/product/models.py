from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):

    name = models.CharField(max_length=200)
    nutriscore = models.CharField(max_length=1, null=True)
    nova = models.IntegerField(null=True)
    url = models.URLField(max_length=200)
    barcode = models.CharField(max_length=200, unique=True)
    description = models.TextField()
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
