from django.db import models
# from django.contrib.auth.models import User
from nutella_fans.product.models import Product


class Substitute(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='choosen_product')
    substitute = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='substitute')

    def __str__(self):
        return self.id
