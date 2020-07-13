import factory
from django.db import models
from factory import Factory
from imagekit.models import ImageSpecField
from pilkit.processors import Thumbnail
from uuid_upload_path import upload_to


class Post(models.Model):
    user_profile = models.ForeignKey('profiles.UserProfile', related_name='user_profiles', on_delete=models.CASCADE)
    post_text = models.TextField(default='')
    time_stamp = models.DateTimeField(auto_now_add=True)
    image_name = models.CharField(max_length=50)
    origin_image = models.ImageField(upload_to=upload_to)  # generate uuid path
    thumbnail_image = ImageSpecField(source='origin_image',
                                     processors=[Thumbnail(161, 161)],
                                     format='JPEG',
                                     options={'quality': 60})


class PostFactory(Factory):
    origin_image = factory.django.ImageField()

    class Meta:
        model = Post
