import factory
from django.db import models
from factory import Factory
from imagekit.models import ImageSpecField
from pilkit.processors import Thumbnail
from uuid_upload_path import upload_to


class Photo(models.Model):
    user = models.ForeignKey('users.User', related_name='owner', on_delete=models.CASCADE)
    post = models.ForeignKey('feeds.Post', related_name='posts', on_delete=models.CASCADE)
    image_name = models.CharField(max_length=50)
    photo_images = models.ImageField(upload_to=upload_to)  # generate uuid path
    thumbnail_image = ImageSpecField(source='photo_images',
                                     processors=[Thumbnail(161, 161)],
                                     format='JPEG',
                                     options={'quality': 60})


class PhotoFactory(Factory):
    photo_images = factory.django.ImageField()

    class Meta:
        model = Photo
