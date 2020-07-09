from django.contrib.postgres.fields import ArrayField
from django.db import models
import tempfile
from PIL import Image


class Photo(models.Model):
    user = models.ForeignKey('users.User', related_name='users', on_delete=models.CASCADE)
    photo_images = ArrayField(models.ImageField(upload_to='photo_images'))
    photo_texts = models.TextField(default='')
    # photo_like = models.ForeignKey('likes.like', related_name='likes', on_delete=models.CASCADE)


