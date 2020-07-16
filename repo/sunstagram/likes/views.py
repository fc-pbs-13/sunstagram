from django.db.models import F
from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet

from comments.models import Comment
from core.permissions import IsOwnerOrReadOnly
from feeds.models import Post
from likes.models import PostLike, CommentLike, ReplyLike
from likes.serializers import PostLikeSerializer, CommentLikeSerializer, ReplyLikeSerializer
from replies.models import Reply


class PostLikeViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    permission_classes = [IsOwnerOrReadOnly, ]

    def filter_queryset(self, queryset):
        if self.action == 'destroy':
            return super().filter_queryset(queryset)
        elif self.kwargs.get('post_pk'):
            queryset = queryset.filter(post_id=self.kwargs['post_pk'])
            return super().filter_queryset(queryset)
        else:
            raise ValueError

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('post_pk'))
        serializer.save(user=self.request.user, post=post)

    def perform_destroy(self, instance):
        Post.objects.filter(id=instance.post.id).update(like_count=F('like_count') - 1)
        instance.delete()


class CommentLikeViewSet(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [IsOwnerOrReadOnly, ]

    def filter_queryset(self, queryset):
        if self.action == 'destroy':
            return super().filter_queryset(queryset)
        elif self.kwargs.get('comment_pk'):
            queryset = queryset.filter(comment_id=self.kwargs['comment_pk'])
            return super().filter_queryset(queryset)
        else:
            raise ValueError

    def perform_create(self, serializer):
        comment = get_object_or_404(Comment, id=self.kwargs.get('comment_pk'))
        serializer.save(user=self.request.user, comment=comment)

    def perform_destroy(self, instance):
        Comment.objects.filter(id=instance.comment.id).update(like_count=F('like_count') - 1)
        instance.delete()


class ReplyLikeViewSet(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    queryset = ReplyLike.objects.all()
    serializer_class = ReplyLikeSerializer
    permission_classes = [IsOwnerOrReadOnly, ]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def filter_queryset(self, queryset):
        if self.action == 'destroy':
            return super().filter_queryset(queryset)
        elif self.kwargs.get('reply_pk'):
            queryset = queryset.filter(reply_id=self.kwargs['reply_pk'])
            return super().filter_queryset(queryset)
        else:
            raise ValueError

    def perform_create(self, serializer):
        reply = get_object_or_404(Reply, id=self.kwargs.get('reply_pk'))
        serializer.save(user=self.request.user, reply=reply)

    def perform_destroy(self, instance):
        Reply.objects.filter(id=instance.reply.id).update(like_count=F('like_count') - 1)
        instance.delete()
