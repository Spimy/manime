from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_profile")
    slug = models.SlugField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to="User_Avatars", null=True, blank=True)
    banner = models.ImageField(upload_to="User_Banners", null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    following = models.ManyToManyField(
        User, related_name="following", blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username
