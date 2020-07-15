from rest_framework import serializers

from likes.models import PostLike
from profiles.serializers import PostingProfileSerializer


class PostLikeSerializer(serializers.ModelSerializer):
    user = PostingProfileSerializer(source='user.userprofile', read_only=True)

    class Meta:
        model = PostLike
        fields = ['id', 'user', 'post']
        read_only_fields = ('id', 'user', 'post')
