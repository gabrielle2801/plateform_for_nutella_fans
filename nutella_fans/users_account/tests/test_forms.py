from django.test import TestCase
from nutella_fans.users_account.forms import UserCreationForm, LoginForm
from nutella_fans.users_account.models import User


class UserFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username='gabrielle', email='gabrielle@email.com', password='12test12')

    def test_userform_valid(self):
        form = UserCreationForm(data={
            'username': 'annie',
            'email': 'annie@email.com',
            'password1': '12test12',
            'password2': '12test12'
        })

        self.assertTrue(form.is_valid())

    def test_invalid_password(self):
        form = UserCreationForm(data={
            'username': 'gabrielle',
            'email': 'gabrielle@email.com',
            'password1': '12test12',
            'password2': '12test'
        })
        self.assertFalse(form.is_valid())


class LoginTest(TestCase):
    def test_login(self):
        form_data = {'username': 'username',
                     'password': 'password'
                     }
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())
