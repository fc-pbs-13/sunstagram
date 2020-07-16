import factory
from django.db import models
from factory import Factory


class UserProfile(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images', default='profile_images/default.jpg')
    web_site = models.URLField(max_length=100, default='')
    intro = models.CharField(max_length=255, default='')
    phone_number = models.CharField(max_length=30, default='')
    following_count = models.PositiveIntegerField(default=0)
    follower_count = models.PositiveIntegerField(default=0)


class ProfileFactory(Factory):
    profile_image = factory.django.ImageField()

    class Meta:
        model = UserProfile
