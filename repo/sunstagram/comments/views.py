from itertools import count

from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from comments.models import Comment
from comments.serializers import CommentSerializer
from core.permissions import IsOwnerOrReadOnly


class CommentViewSet(mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     GenericViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly, ]

    def filter_queryset(self, queryset):
        if self.action == 'destroy':
            return super().filter_queryset(queryset)
        queryset = queryset.filter(post_id=self.kwargs['post_pk'])
        return super().filter_queryset(queryset)

    def perform_create(self, serializer):
        post_id = self.kwargs['post_pk']
        serializer.save(user=self.request.user, post_id=post_id)
