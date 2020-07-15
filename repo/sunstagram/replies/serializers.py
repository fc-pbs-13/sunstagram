from rest_framework import serializers

from profiles.serializers import PostingProfileSerializer
from replies.models import Reply


class ReplySerializer(serializers.ModelSerializer):
    user = PostingProfileSerializer(source='user.userprofile', read_only=True)

    class Meta:
        model = Reply
        fields = ['id', 'reply_text', 'time_stamp', 'user']
        read_only_fields = ('id', 'time_stamp', 'user')

