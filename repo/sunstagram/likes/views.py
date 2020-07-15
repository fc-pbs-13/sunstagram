from django.db.models import F
from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet

from core.permissions import IsOwnerOrReadOnly
from feeds.models import Post
from likes.models import PostLike
from likes.serializers import PostLikeSerializer


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
