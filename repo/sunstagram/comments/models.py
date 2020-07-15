from django.db import models


class Comment(models.Model):
    user = models.ForeignKey('users.User', related_name='comment_owners', on_delete=models.CASCADE)
    post = models.ForeignKey('feeds.Post', related_name='commented_posts', on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=255)
    time_stamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
