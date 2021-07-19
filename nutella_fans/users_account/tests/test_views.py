# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse


class BaseTest(TestCase):
    def setUp(self):
        User = get_user_model()
        self.login_url = reverse('login')
        self.signup_url = reverse('sign_up')
        self.logout_url = reverse('logout')
        self.user = User.objects.create_user(
            username='test', password='12test12', email='test@email.com')
        self.user = {
            'username': 'username',
            'password1': 'password@1234',
            'password2': 'password@1234',
            'email': 'testemail@gmail.com'
        }
        self.user_unmatching_password = {
            'username': 'test',
            'password1': '12test12',
            'password2': '1test12',
            'email': 'testemail@email.com'
        }
        self.user_email_invalid = {
            'username': 'test',
            'password1': '12test12',
            'password2': '12test12',
            'email': 'testemail.com'
        }
        self.user_login = {
            'username': 'test',
            'password': '12test12'
        }
        return super().setUp()


class SignUpTest(BaseTest):
    def test_view_ok(self):
        response = self.client.get(self.signup_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'registration/sign_up.html')

    def test_can_signup(self):
        response = self.client.post(
            self.signup_url, self.user)
        self.assertEquals(response.status_code, 302)

    def test_unmatching_password(self):
        response = self.client.post(
            self.signup_url, self.user_unmatching_password)
        self.assertEquals(response.status_code, 200)

    def test_invalid_email(self):
        response = self.client.post(
            self.signup_url, self.user_email_invalid)
        self.assertEquals(response.status_code, 200)


class LoginTest(BaseTest):

    def test_can_view_page_correctly(self):
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(
            response, 'registration/login.html')

    def test_login_sucess(self):
        response = self.client.post(
            self.login_url, self.user_login, follow=True)
        self.assertTrue(response.context['user'].is_active)


class LogoutTest(BaseTest):
    def test_user_logout(self):
        response = self.client.post(self.login_url, follow=True)
        self.assertFalse(response.context['user'].is_active)
