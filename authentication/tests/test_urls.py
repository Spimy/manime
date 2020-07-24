from django.test import SimpleTestCase
from django.urls import resolve, reverse
from ..views import LoginView, RegisterView, LogoutView


class TestUrls(SimpleTestCase):

    def test_login_url_resolves(self):
        url = reverse('authentication:login')
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_register_url_resolves(self):
        url = reverse('authentication:register')
        self.assertEqual(resolve(url).func.view_class, RegisterView)

    def test_logout_url_resolves(self):
        url = reverse('authentication:logout')
        self.assertEqual(resolve(url).func.view_class, LogoutView)
