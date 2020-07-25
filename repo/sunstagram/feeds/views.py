from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from core.permissions import IsOwnerOrReadOnly
from feeds.models import Post, HashTag, TagPostList
from feeds.serializers import PostSerializer, HashTagSerializer, TagPostListSerializer, PostWithTagSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly, ]

    def create(self, request, *args, **kwargs):
        """
        tag 포함 요청일 경우 시리얼라이저 변경
        """
        if request.data.get('tag'):
            self.serializer_class = PostWithTagSerializer
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        """
        tag 포함 요청일 경우 시리얼라이저 변경
        """
        if request.data.get('tag'):
            self.serializer_class = PostWithTagSerializer
        return super().update(request, *args, **kwargs)


class HashTagViewSet(ModelViewSet):
    queryset = TagPostList.objects.all()
    serializer_class = TagPostListSerializer
    permission_classes = [IsOwnerOrReadOnly, ]

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs.get('post_pk'))
        serializer.save(user=self.request.user, post=post)
