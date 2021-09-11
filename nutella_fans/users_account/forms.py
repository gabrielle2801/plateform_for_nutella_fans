from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserCreationForm(UserCreationForm):

    """Creation of users's account

    Attributes:
        email (TYPE): Description
    """

    email = forms.EmailField(required=True)

    class Meta:

        """ Form's fields

        Attributes:
            fields (tuple): Description
            model (TYPE): User's model
        """

        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(forms.Form):

    """ Class user's login

    Attributes:
        password (str): Description
        username (str): Description
    """

    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput)

    class Meta:

        """Summary

        Attributes:
            fields (tuple): Description
            model (TYPE): Description
        """

        model = User
        fields = ('username', 'password')
