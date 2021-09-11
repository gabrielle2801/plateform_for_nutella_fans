"""Summary
"""
from django.db import models
from nutella_fans.product.models import Product


class Substitute(models.Model):

    """Subtitute Model save the favorite product called substitute

    Attributes:
        product (INT): ID of unhealthy product
        substitute (INT): ID of unhealthy product
    """

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='choosen_product')
    substitute = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='substitute')

    def __str__(self):
        return self.id
