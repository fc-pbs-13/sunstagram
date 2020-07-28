import datetime

from django.db.models import Q
from django.utils import timezone
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from stories.models import Story, StoryViewCheck
from stories.serializers import StorySerializer
from users.models import User


class StoryViewSet(ModelViewSet):
    queryset = Story.objects.all().select_related('user__userprofile')
    serializer_class = StorySerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action == 'list':
            now = timezone.now()
            _min = now - datetime.timedelta(days=1)
            queryset = queryset.filter(Q(user=self.request.user)
                                       | Q(user__in=User.objects.filter(followings__follower=self.request.user)))
            queryset = queryset.filter(time_stamp__gte=_min)

        return queryset

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            StoryViewCheck.objects.get_or_create(user=request.user, story_id=response.data.get('id'))
        return response





