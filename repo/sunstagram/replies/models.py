from django.db import models


class Reply(models.Model):
    user = models.ForeignKey('users.User', related_name='replied_owners', on_delete=models.CASCADE)
    comment = models.ForeignKey('comments.Comment', related_name='replies', on_delete=models.CASCADE)
    reply_text = models.CharField(max_length=255)
    time_stamp = models.DateTimeField(auto_now_add=True)
