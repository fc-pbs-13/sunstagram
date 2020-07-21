from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from likes.models import PostLike, CommentLike, ReplyLike
from profiles.serializers import PostingProfileSerializer


class PostLikeSerializer(serializers.ModelSerializer):
    user = PostingProfileSerializer(source='user.userprofile', read_only=True)

    class Meta:
        model = PostLike
        fields = ['id', 'user', 'post']
        read_only_fields = ('id', 'user', 'post')

    def validate(self, attrs):
        if PostLike.objects.filter(user=self.context['request'].user,
                                   post=self.context['view'].kwargs['post_pk']).exists():
            raise serializers.ValidationError('The fields `user`, `reply` must make a unique set.',
                                              code='unique')
        return super().validate(attrs)


class CommentLikeSerializer(serializers.ModelSerializer):
    user = PostingProfileSerializer(source='user.userprofile', read_only=True)

    class Meta:
        model = CommentLike
        fields = ['id', 'user', 'comment']
        read_only_fields = ('id', 'user', 'comment')

    def validate(self, attrs):
        if CommentLike.objects.filter(user=self.context['request'].user,
                                      comment=self.context['view'].kwargs['comment_pk']).exists():
            raise serializers.ValidationError('The fields `user`, `reply` must make a unique set.',
                                              code='unique')
        return super().validate(attrs)


class ReplyLikeSerializer(serializers.ModelSerializer):
    user = PostingProfileSerializer(source='user.userprofile', read_only=True)

    class Meta:
        model = ReplyLike
        fields = ['id', 'user', 'reply']
        read_only_fields = ('id', 'user', 'reply')

    def validate(self, attrs):
        if ReplyLike.objects.filter(user=self.context['request'].user,
                                    reply=self.context['view'].kwargs['reply_pk']).exists():
            raise serializers.ValidationError('The fields `user`, `reply` must make a unique set.',
                                              code='unique')
        return super().validate(attrs)
