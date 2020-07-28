import datetime
from time import sleep

from django.core.cache import cache
from django.db.models import F
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from core.permissions import IsFollowerSelfOrReadOnly
from follows.models import Follow, Parent
from follows.serializers import FollowSerializer, ParentSerializer
from profiles.models import UserProfile
from users.models import User


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    """
    url - post : users/12/follows (request.user following user_12)
        - list : users/12/follows (Follow.following.filter(following_id=user_12.id))
        - delete : follows/23 (request.user unfollowing user_23)
    """
    queryset = Follow.objects.all().select_related('follower__userprofile')
    serializer_class = FollowSerializer
    permission_classes = [IsFollowerSelfOrReadOnly, ]

    def perform_create(self, serializer):
        following = get_object_or_404(User, id=self.kwargs.get('user_pk'))
        serializer.save(follower=self.request.user, following=following)


class ParentViewSet(ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer
    permission_classes = [AllowAny, ]

    @method_decorator(cache_page(60 * 60 * 2))
    def list(self, request, *args, **kwargs):
        key = 'my_key'
        val = cache.get('key')

        if not val:
            sleep(3)
            val = 'fast-campus'
            cache.set(key, val, 60)
            data = {
                'my_data': val,
            }
        return Response(data=data)
