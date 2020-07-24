from django.db import models
from django.db.models import F


class Post(models.Model):
    user = models.ForeignKey('users.User', related_name='users', on_delete=models.CASCADE)
    post_text = models.TextField(default='')
    time_stamp = models.DateTimeField(auto_now_add=True)
    like_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-id']


class HashTag(models.Model):
    name = models.CharField(max_length=12, unique=True)
    tag_count = models.PositiveIntegerField(default=0)


class TagPostList(models.Model):
    post = models.ForeignKey('feeds.Post', related_name='tagged_posts', on_delete=models.CASCADE)
    tag = models.ForeignKey('feeds.HashTag', related_name='posted_tags', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['post', 'tag']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        HashTag.objects.filter(tag_id=self.tag.id).update(tag_count=F('tag_count') + 1)

    def delete(self, using=None, keep_parents=False):
        deleted = super().delete(using, keep_parents)
        HashTag.objects.filter(tag_id=self.tag.id).update(tag_count=F('tag_count') - 1)
        return deleted
