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
        if self.action == 'list':
            queryset = queryset.filter(post_id=self.kwargs.get('post_pk'))
        return super().filter_queryset(queryset)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('post_pk'))
        serializer.save(user=self.request.user, post=post)


class CommentLikeViewSet(mixins.CreateModelMixin,
                         mixins.DestroyModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [IsOwnerOrReadOnly, ]

    def filter_queryset(self, queryset):
        if self.action == 'list':
            queryset = queryset.filter(comment_id=self.kwargs.get('comment_pk'))
        return super().filter_queryset(queryset)

    def perform_create(self, serializer):
        comment = get_object_or_404(Comment, id=self.kwargs.get('comment_pk'))
        serializer.save(user=self.request.user, comment=comment)


class ReplyLikeViewSet(mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    queryset = ReplyLike.objects.all().select_related('user__userprofile')
    serializer_class = ReplyLikeSerializer
    permission_classes = [IsOwnerOrReadOnly, ]

    def filter_queryset(self, queryset):
        if self.action == 'list':
            queryset = queryset.filter(reply_id=self.kwargs.get('reply_pk'))
        return super().filter_queryset(queryset)

    def perform_create(self, serializer):
        reply = get_object_or_404(Reply, id=self.kwargs.get('reply_pk'))
        serializer.save(user=self.request.user, reply=reply)
