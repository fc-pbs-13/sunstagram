from django.db import models
from django.db.models import F

from comments.models import Comment
from feeds.models import Post
from replies.models import Reply


class PostLike(models.Model):
    user = models.ForeignKey('users.User', related_name='post_likes_users', on_delete=models.CASCADE)
    post = models.ForeignKey('feeds.Post', related_name='post_likes', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']
        unique_together = ['user', 'post']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        Post.objects.filter(id=self.post.id).update(like_count=F('like_count') + 1)

    def delete(self, using=None, keep_parents=False):
        super().delete(using, keep_parents)
        Post.objects.filter(id=self.post.id).update(like_count=F('like_count') - 1)


class CommentLike(models.Model):
    user = models.ForeignKey('users.User', related_name='comment_likes_users', on_delete=models.CASCADE)
    comment = models.ForeignKey('comments.Comment', related_name='comment_likes', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']
        unique_together = ['user', 'comment']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        Comment.objects.filter(id=self.comment.id).update(like_count=F('like_count') + 1)

    def delete(self, using=None, keep_parents=False):
        super().delete(using, keep_parents)
        Comment.objects.filter(id=self.comment.id).update(like_count=F('like_count') - 1)


class ReplyLike(models.Model):
    user = models.ForeignKey('users.User', related_name='reply_likes_users', on_delete=models.CASCADE)
    reply = models.ForeignKey('replies.Reply', related_name='reply_likes', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']
        unique_together = ['user', 'reply']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        Reply.objects.filter(id=self.reply.id).update(like_count=F('like_count') + 1)

    def delete(self, using=None, keep_parents=False):
        super().delete(using, keep_parents)
        Reply.objects.filter(id=self.reply.id).update(like_count=F('like_count') - 1)
