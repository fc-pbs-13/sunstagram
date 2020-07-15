from django.db import models
from django.db.models import F
from feeds.models import Post


class PostLike(models.Model):
    user = models.ForeignKey('users.User', related_name='post_likes_users', on_delete=models.CASCADE)
    post = models.ForeignKey('feeds.Post', related_name='post_likes', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']
        unique_together = ['user', 'post']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.id is None:
            Post.objects.filter(id=self.post.id).update(like_count=F('like_count') + 1)
        else:
            raise ValueError
        return super().save()
