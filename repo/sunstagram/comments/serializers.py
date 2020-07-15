from rest_framework import serializers

from comments.models import Comment
from profiles.serializers import PostingProfileSerializer


class CommentSerializer(serializers.ModelSerializer):
    user = PostingProfileSerializer(source='user.userprofile', read_only=True)
    reply_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'comment_text', 'time_stamp', 'user', 'reply_count']
        read_only_fields = ('id', 'time_stamp', 'user', 'reply_count')

    def get_reply_count(self, obj):
        return obj.replies.count()
