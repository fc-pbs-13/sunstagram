from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from core.permissions import IsOwnerOrReadOnly
from feeds.models import Post
from feeds.serializers import PostSerializer


class PostViewSet(ModelViewSet):

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly, ]

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [AllowAny()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
