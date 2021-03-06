from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet

from comments.models import Comment
from replies.models import Reply
from replies.serializers import ReplySerializer
from core.permissions import IsOwnerOrReadOnly


class ReplyViewSet(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    queryset = Reply.objects.all().select_related('user__userprofile')
    serializer_class = ReplySerializer
    permission_classes = [IsOwnerOrReadOnly, ]

    def filter_queryset(self, queryset):
        if self.action == 'list':
            queryset = queryset.filter(comment_id=self.kwargs.get('comment_pk'))
        return super().filter_queryset(queryset)

    def perform_create(self, serializer):
        comment = get_object_or_404(Comment, id=self.kwargs.get('comment_pk'))
        serializer.save(user=self.request.user, comment=comment)
