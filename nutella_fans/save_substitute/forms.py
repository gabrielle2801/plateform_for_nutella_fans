"""Summary
"""
from django import forms

from nutella_fans.save_substitute.models import Substitute


class FavoriteCreateForm(forms.ModelForm):

    """
    Hide form to get id of healthy and unhealthy product
    """

    class Meta:

        """Summary

        Attributes:
            fields (list): Description
            model (model class): Substitute model
        """

        model = Substitute
        fields = ['product', 'substitute']
