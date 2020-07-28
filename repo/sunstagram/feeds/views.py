from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from core.permissions import IsOwnerOrReadOnly
from feeds.models import Post, TagPostList, HashTag
from feeds.serializers import PostSerializer, TagPostListSerializer, TagShowSerializer, HashTagSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().select_related('user__userprofile').\
        prefetch_related('tagged_posts__tag', 'photo_posts')

    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TagPostViewSet(mixins.DestroyModelMixin, GenericViewSet):
    queryset = TagPostList.objects.all()
    serializer_class = TagPostListSerializer

    def destroy(self, request, *args, **kwargs):
        get_object_or_404(Post, id=self.kwargs.get('post_pk'))
        return super().destroy(request, *args, **kwargs)


class SearchTagViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = HashTag.objects.all()
    serializer_class = HashTagSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = HashTag.objects.filter(name__startswith=keyword)
        return queryset

    @action(detail=True)
    def posts(self, request, **kwargs):
        get_object_or_404(HashTag, id=kwargs.get('pk'))

        queryset = Post.objects.filter(tagged_posts__tag=kwargs['pk'])
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
