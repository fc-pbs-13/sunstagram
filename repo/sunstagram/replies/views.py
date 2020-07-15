from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from replies.models import Reply
from replies.serializers import ReplySerializer
from core.permissions import IsOwnerOrReadOnly


class ReplyViewSet(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):

    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [IsOwnerOrReadOnly, ]

    def filter_queryset(self, queryset):
        if self.action == 'destroy':
            return super().filter_queryset(queryset)
        queryset = queryset.filter(comment_id=self.kwargs['comment_pk'])
        return super().filter_queryset(queryset)

    def perform_create(self, serializer):
        comment_id = self.kwargs['comment_pk']
        serializer.save(user=self.request.user, comment_id=comment_id)
