from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import UserProfile


def create_profile(sender, **kwargs):
    if kwargs.get("created", False):
        user_profile = UserProfile.objects.create(user=kwargs["instance"])


post_save.connect(create_profile, User)
