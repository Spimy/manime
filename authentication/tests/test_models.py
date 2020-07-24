from django.test import TestCase
from django.contrib.auth import get_user_model
from ..models import UserProfile


class TestModels(TestCase):

    def setUp(self):

        self.credentials = {
            'username': 'ZRealTDW',
            'password': 'GoodEnoughPassword!Ithink50...'
        }

        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(**self.credentials)

    def test_profile_is_created(self):
        self.assertIsNotNone(self.user.user_profile)

        user_profile = UserProfile.objects.all()
        self.assertEqual(user_profile.count(), 1)

    def test_profile_slug_is_assgned(self):
        self.assertEqual(self.user.user_profile.slug, 'zrealtdw')
