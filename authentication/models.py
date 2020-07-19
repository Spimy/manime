from django.db import models
from django.conf import settings
from django.utils.text import slugify

# Create your models here.


class UserProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_profile'
    )

    slug = models.SlugField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(upload_to='User_Avatars', null=True, blank=True)
    banner = models.ImageField(upload_to='User_Banners', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    following = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='following',
        blank=True
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username
