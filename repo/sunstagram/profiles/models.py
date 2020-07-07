from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images', default='profile_images/default.jpg')
    web_site = models.URLField(max_length=100, blank=True)
    intro = models.CharField(max_length=300, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
