from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from core.permissions import IsOwnerOrReadOnly
from feeds.models import Post, HashTag, TagPostList
from feeds.serializers import PostSerializer, HashTagSerializer, TagPostListSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HashTagViewSet(ModelViewSet):
    queryset = TagPostList.objects.all()
    serializer_class = TagPostListSerializer
    permission_classes = [IsOwnerOrReadOnly, ]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('post_pk'))
        serializer.save(user=self.request.user, post=post)
