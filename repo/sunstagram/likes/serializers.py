from rest_framework import serializers

from likes.models import PostLike, CommentLike, ReplyLike
from profiles.serializers import PostingProfileSerializer


class PostLikeSerializer(serializers.ModelSerializer):
    user = PostingProfileSerializer(source='user.userprofile', read_only=True)

    class Meta:
        model = PostLike
        fields = ['id', 'user', 'post']
        read_only_fields = ('id', 'user', 'post')


class CommentLikeSerializer(serializers.ModelSerializer):
    user = PostingProfileSerializer(source='user.userprofile', read_only=True)

    class Meta:
        model = CommentLike
        fields = ['id', 'user', 'comment']
        read_only_fields = ('id', 'user', 'comment')


class ReplyLikeSerializer(serializers.ModelSerializer):
    user = PostingProfileSerializer(source='user.userprofile', read_only=True)

    class Meta:
        model = ReplyLike
        fields = ['id', 'user', 'reply']
        read_only_fields = ('id', 'user', 'reply')

