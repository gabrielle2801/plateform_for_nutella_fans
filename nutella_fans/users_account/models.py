"""Summary
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from nutella_fans.save_substitute.models import Substitute


class User(AbstractUser):

    """Summary

    Attributes:
        substitutes (TYPE): Relationship between user and substitutes
        model
    """

    substitutes = models.ManyToManyField(Substitute)

    def __str__(self):
        """Summary

        Returns:
            TYPE: email
        """
        return self.email
