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
        super().delete(using, keep_parents)
        UserProfile.objects.filter(user_id=self.follower.id).update(following_count=F('following_count') - 1)
        UserProfile.objects.filter(user_id=self.following.id).update(follower_count=F('follower_count') - 1)
