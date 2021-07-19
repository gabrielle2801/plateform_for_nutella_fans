from django.db import models
from django.contrib.auth.models import AbstractUser
from nutella_fans.save_substitute.models import Substitute


class User(AbstractUser):

    substitutes = models.ManyToManyField(Substitute)

    def __str__(self):
        return self.email
