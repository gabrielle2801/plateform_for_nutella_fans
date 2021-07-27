from django import forms

from nutella_fans.save_substitute.models import Substitute


class FavoriteCreateForm(forms.ModelForm):
    class Meta:
        model = Substitute
        fields = ['product', 'substitute']
