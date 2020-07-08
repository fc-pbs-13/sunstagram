from django.db import models


class Photo(models.Model):
    user = models.ForeignKey('users.User', related_name='users', on_delete=models.CASCADE)
    photo_images = models.ImageField(upload_to='photo_images')
    photo_texts = models.TextField(blank=True)
    # photo_like = models.ForeignKey('likes.like', related_name='likes', on_delete=models.CASCADE)
