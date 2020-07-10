import tempfile

import factory
from PIL.Image import Image
from django.contrib.postgres.fields import ArrayField
from django.db import models
from factory import Factory

from sunstagram.settings.base import MEDIA_ROOT


class Photo(models.Model):
    user = models.ForeignKey('users.User', related_name='users', on_delete=models.CASCADE)
    photo_texts = models.TextField(default='')
    photo_images = ArrayField(models.ImageField(upload_to='photo_images'))
    # photo_thumbnail = ArrayField(models.ImageField(upload_to='photo_images'))
    # photo_like = models.ForeignKey('likes.like', related_name='likes', on_delete=models.CASCADE)


class PhotoFactory(Factory):
    class Meta:
        model = Photo

    photo_images = factory.django.ImageField(width=1)
    # def create_test_image(self):
    #     image = Image.new('RGB', (1, 1))
    #     tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    #     image.save(tmp_file, 'jpeg')
    #     tmp_file.seek(0)
    #     return tmp_file

