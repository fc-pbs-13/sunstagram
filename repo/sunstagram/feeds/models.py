from django.db import models


class Post(models.Model):
    user = models.ForeignKey('users.User', related_name='users', on_delete=models.CASCADE)
    post_text = models.TextField(default='')
    time_stamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
