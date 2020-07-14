from rest_framework import mixins, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from core.permissions import IsOwnerOrReadOnly
from photos.models import Photo
from photos.serializers import PhotoSerializer


class PhotoViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_permissions(self):
        if self.action == 'retrieve':
            return [AllowAny()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)