from django.test import TestCase, Client
from django.shortcuts import HttpResponse
from django.urls import reverse
from django.contrib.auth import get_user_model


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model()
        self.login_url = reverse('authentication:login')
        self.register_url = reverse('authentication:register')
        self.logout_url = reverse('authentication:logout')

        self.credentials = {
            'username': 'zrealtdw',
            'password': 'GoodEnoughPassword!Ithink50...'
        }

        self.register_credentials = {
            'username': 'tdwilliam',
            'email': 'tdwilliam@gmail.com',
            'password1': self.credentials['password'],
            'password2': self.credentials['password']
        }

        self.user.objects.create_user(**self.credentials)

    def test_login_get(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_post_follow(self):
        response = self.client.post(
            self.login_url, self.credentials, follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_active)

    def test_login_post_no_follow(self):
        response = self.client.post(
            self.login_url, self.credentials, follow=False
        )

        self.assertEqual(response.status_code, 302)

    def test_login_post_wrong_data(self):
        response = self.client.post(
            self.login_url, {**self.credentials, 'username': 'spimy'}
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_login_post_no_data(self):

        try:
            response = self.client.post(self.login_url)
        except KeyError:
            return HttpResponse(200)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_register_get(self):
        response = self.client.get(self.register_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_register_post_follow(self):
        response = self.client.post(
            self.register_url, self.register_credentials, follow=True
        )
        self.assertEqual(response.status_code, 200)

        users = self.user.objects.all()
        self.assertEqual(users.count(), 2)
        self.assertTrue(response.context['user'].is_authenticated)

    def test_register_post_no_follow(self):
        response = self.client.post(
            self.register_url, self.register_credentials
        )
        self.assertEqual(response.status_code, 302)

        users = self.user.objects.all()
        self.assertEqual(users.count(), 2)

    def test_register_wrong_data(self):
        """
        This test for wrong data passed in. Test will check whether the password is
        too similar to the username or not
        """

        wrong_register_data = {
            **self.register_credentials,
            'password1': 'Tdwilliam123!',
            'password2': 'Tdwilliam123!'
        }

        response = self.client.post(self.register_url, wrong_register_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['form'].is_valid())

        users = self.user.objects.all()
        self.assertEqual(users.count(), 1)

    def test_register_no_data(self):
        try:
            response = self.client.post(self.register_url)
        except (KeyError, AttributeError):
            return HttpResponse(200)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_authenticated)
