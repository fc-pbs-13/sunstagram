from django.db.models import F
from rest_framework import mixins
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet

from core.permissions import IsFollowerSelfOrReadOnly
from follows.models import Follow
from follows.serializers import FollowSerializer
from profiles.models import UserProfile
from users.models import User


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    """
    url - post : users/12/follows (request.user following user_12)
        - list : users/12/follows (Follow.following.filter(following_id=user_12.id))
        - delete : follows/23 (request.user unfollowing user_23)
    """
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsFollowerSelfOrReadOnly, ]

    def filter_queryset(self, queryset):
        if self.action == 'destroy':
            return super().filter_queryset(queryset)
        elif self.kwargs.get('user_pk'):
            queryset = queryset.filter(following_id=self.kwargs['user_pk'])
            return super().filter_queryset(queryset)
        else:
            raise ValueError

    def perform_create(self, serializer):
        following = get_object_or_404(User, id=self.kwargs.get('user_pk'))
        serializer.save(follower=self.request.user, following=following)

    def perform_destroy(self, instance):
        UserProfile.objects.filter(user_id=instance.follower.id).update(following_count=F('following_count') - 1)
        UserProfile.objects.filter(user_id=instance.following.id).update(follower_count=F('follower_count') - 1)
        instance.delete()
