from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from ..forms import LoginForm, RegistrationForm


class TestForms(TransactionTestCase):

    def setUp(self):
        self.user = get_user_model()
        self.credentials = {
            'username': 'zrealtdw',
            'password': 'GoodEnoughPassword!Ithink50...'
        }
        self.user.objects.create_user(**self.credentials)

    def test_login_form_is_valid(self):
        form = LoginForm(data=self.credentials)
        self.assertTrue(form.is_valid())

    def test_login_form_no_data(self):
        form = LoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)

    def test_register_form_is_valid(self):
        register_credentials = {
            'username': 'tdwilliam',
            'email': 'tdwilliam@gmail.com',
            'password1': self.credentials['password'],
            'password2': self.credentials['password']
        }

        form = RegistrationForm(data=register_credentials)
        self.assertTrue(form.is_valid())

    def test_register_form_no_data(self):
        try:
            form = RegistrationForm(data={})
            self.assertFalse(form.is_valid())
            self.assertEqual(len(form.errors), 4)
        except AttributeError:
            pass
