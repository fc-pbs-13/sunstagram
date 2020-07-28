from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet
from comments.models import Comment
from comments.serializers import CommentSerializer
from core.permissions import IsOwnerOrReadOnly
from feeds.models import Post


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):

    queryset = Comment.objects.all().select_related('user__userprofile')
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly, ]

    def filter_queryset(self, queryset):
        if self.action == 'list':
            queryset = queryset.filter(post_id=self.kwargs.get('post_pk'))
        return super().filter_queryset(queryset)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('post_pk'))
        serializer.save(user=self.request.user, post=post)
