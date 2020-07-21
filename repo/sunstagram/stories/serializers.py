from rest_framework import serializers

from profiles.serializers import PostingProfileSerializer
from stories.models import Story


class StorySerializer(serializers.ModelSerializer):
    user = PostingProfileSerializer(source='user.userprofile', read_only=True)

    class Meta:
        model = Story
        fields = ['id', 'story_text', 'time_stamp', 'story_image', 'image_name', 'user']
        read_only_fields = ('id', 'time_stamp', 'image_name', 'user')

