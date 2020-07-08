from rest_framework import mixins, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.permissions import IsOwner, IsUserSelf
from users.models import User
from users.serializers import UserSerializer, PasswordSerializer


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUserSelf, ]

    def get_serializer_class(self):
        if self.action == 'change_password':
            return PasswordSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ('sign_in', 'create'):
            return [AllowAny()]
        return super().get_permissions()

    @action(detail=True, methods=['PATCH'])
    def change_password(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        current_password = request.data.get('password')
        password = request.data.get('new_password')
        password2 = request.data.get('new_password')

        if user.password == current_password:
            if password == password2:
                user.set_password(password)
                user.save()
                data = {"hashed_password": user.password}
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                data = {"message": "Not matched password and password2"}
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

        data = {"message": "incorrect current_password"}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def sign_in(self, request):
        password = request.data.get('password')
        user = User.objects.get(email=request.data.get('email'),
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
