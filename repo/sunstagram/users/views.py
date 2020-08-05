from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.permissions import IsUserSelf
from follows.models import Follow
from follows.serializers import FollowingListSerializer, FollowersListSerializer
from users.models import User
from users.serializers import UserSerializer, PasswordSerializer


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUserSelf, ]

    def get_serializer_class(self):
        if self.action == 'change_password':
            return PasswordSerializer
        elif self.action == 'following':
            return FollowingListSerializer
        elif self.action == 'followers':
            return FollowersListSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ('sign_in', 'create', 'following', 'followers'):
            return [AllowAny()]
        return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'following':
            # users/1/following : 1번유저의 following 목록
            get_object_or_404(User, id=self.kwargs.get('pk'))
            return User.objects.filter(followers__following_id=self.kwargs.get('pk'))
        elif self.action == 'followers':
            # users/1/followers : 1번유저의 follower 목록
            get_object_or_404(User, id=self.kwargs.get('pk'))
            return User.objects.filter(followings__follower_id=self.kwargs.get('pk'))
        return queryset

    @action(detail=True, methods=['PATCH'])
    def change_password(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def sign_in(self, request):
        password = request.data.get('password')
        user = get_object_or_404(User, email=request.data.get('email'),
                                 username=request.data.get('username'))

        if user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key,
                             'id': user.id,
                             'email': user.email,
                             'username': user.username,
                             },
                            status=status.HTTP_201_CREATED)
        data = {
            "message": "incorrect password"
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['DELETE'])
    def sign_out(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['DELETE'])
    def deactivate(self, request, *args, **kwargs):
        return super().destroy(self, request, *args, **kwargs)

    @action(detail=True, methods=['GET'])
    def following(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['GET'])
    def followers(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        return Response(status.HTTP_403_FORBIDDEN)

