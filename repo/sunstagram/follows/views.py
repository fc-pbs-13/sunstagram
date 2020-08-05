import datetime
from time import sleep

from django.core.cache import cache
from django.core.mail import send_mail
from django.db.models import F
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import mixins
from rest_framework.decorators import action
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

    # def function2(self, a, b, c='name'):
    #     aa = 100
    #     bb = 'abc'
    #     cc = { 'val': aa}
    #     0/0
    #
    # @action(detail=False, methods=['GET'])
    # def function(self, req):
        # a = 10
        # b = 2
        # self.function2(a, 0, c='abc')
        # send_mail(
        #     'test email',
        #     'function called!',
        #     'hsw0905@gmail.com',
        #     ['hsw0905@gmail.com'],
        #     fail_silently=False,
        # )


# def retrieve(self, request, *args, **kwargs):
    #     pk = kwargs.get('pk')
    #     if cache.get(f'Parent-instance{pk}') is None:
    #         instance = self.get_object()
    #         cache.set(f'Parent-instance{pk}', instance, 60)
    #     else:
    #         instance = cache.get(f'Parent-instance{pk}')
    #
    #     # May raise a permission denied
    #     self.check_object_permissions(self.request, instance)
    #     # cache.get_or_set(f'Parent-instance{pk}', instance, 60)
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)

# @method_decorator(cache_page(60 * 60 * 2))
# def list(self, request, *args, **kwargs):
#     key = 'my_key'
#     val = cache.get('key')
#
#     if not val:
#         sleep(3)
#         val = 'fast-campus'
#         cache.set(key, val, 60)
#         data = {
#             'my_data': val,
#         }
#     return Response(data=data)
