from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from core.permissions import IsOwner
from profiles.models import UserProfile
from profiles.serializers import UserProfileSerializer


class UserProfileViewSet(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         GenericViewSet):
    queryset = UserProfile.objects.all().select_related('user')
    serializer_class = UserProfileSerializer

    permission_classes = [IsOwner, ]

    def get_permissions(self):
        if self.action == 'retrieve':
            return [AllowAny()]
        return super().get_permissions()
