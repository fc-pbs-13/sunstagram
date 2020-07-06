from django.db import models

# Create your models here.
from accounts.models import Account


class AccountProfile(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    profileImage = models.ImageField(upload_to='profile_images', null=True, blank=True)
    webSite = models.URLField(max_length=100, blank=True)
    intro = models.CharField(max_length=300, blank=True)
    phoneNumber = models.CharField(max_length=30, blank=True)
