from django.test import TestCase

from nutella_fans.save_substitute.forms import FavoriteCreateForm
from nutella_fans.save_substitute.models import Substitute


class FavoriteFormTest(TestCase):
    def setUp(self):
        self.favorite = Substitute.objects.create(
            product_id=1, substitute_id=2)

    def test_favorite_valid(self):
        form = FavoriteCreateForm(data={
            'product_id': 1,
            'substitute_id': 2
        })
        self.assertTrue(form.is_valid())
