from django.db import models
from django.db.models import F

from comments.models import Comment


class Reply(models.Model):
    user = models.ForeignKey('users.User', related_name='replied_owners', on_delete=models.CASCADE)
    comment = models.ForeignKey('comments.Comment', related_name='replies', on_delete=models.CASCADE)
    reply_text = models.CharField(max_length=255)
    time_stamp = models.DateTimeField(auto_now_add=True)
    like_count = models.PositiveIntegerField(default=0)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        Comment.objects.filter(id=self.comment.id).update(reply_count=F('reply_count') + 1)
        return super().save()
