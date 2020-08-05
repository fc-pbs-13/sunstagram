from uuid import uuid4

from django.core.cache import cache
from django.db import models
from django.db.models import F

from profiles.models import UserProfile


class Follow(models.Model):
    follower = models.ForeignKey('users.User', related_name='followers', on_delete=models.CASCADE)
    following = models.ForeignKey('users.User', related_name='followings', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['follower', 'following']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        UserProfile.objects.filter(user_id=self.follower.id).update(following_count=F('following_count') + 1)
        UserProfile.objects.filter(user_id=self.following.id).update(follower_count=F('follower_count') + 1)

    def delete(self, using=None, keep_parents=False):
        deleted = super().delete(using, keep_parents)
        UserProfile.objects.filter(user_id=self.follower.id).update(following_count=F('following_count') - 1)
        UserProfile.objects.filter(user_id=self.following.id).update(follower_count=F('follower_count') - 1)
        return deleted


class Parent(models.Model):
    uuid = models.UUIDField(default=uuid4())

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        # pk = self.id
        super().save(force_insert, force_update, using, update_fields)
        # if pk:
        #     cache.delete(f'Parent-instance{pk}')

    def delete(self, using=None, keep_parents=False):
        # pk = self.id
        deleted = super().delete(using, keep_parents)
        # cache.delete(f'Parent-instance{pk}')
        return deleted


class Child(models.Model):
    uuid = models.UUIDField(default=uuid4())
    parent = models.ForeignKey('follows.Parent', related_name='parents', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey('users.User', related_name='child_users', on_delete=models.CASCADE, null=True)
