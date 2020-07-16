from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from likes.models import PostLike, CommentLike, ReplyLike
from profiles.serializers import PostingProfileSerializer
from replies.models import Reply


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

        # 이거 넣으면 duplicate test에서 400 error를 리턴하지만,
        # create test에서도 400 error를 리턴, serializer.instance가 왜 none인지..
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=ReplyLike.objects.all(),
        #         fields=['user', 'reply']
        #     )
        # ]
