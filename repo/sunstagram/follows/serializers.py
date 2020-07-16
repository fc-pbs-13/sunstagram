from rest_framework import serializers

from follows.models import Follow
from profiles.serializers import PostingProfileSerializer


class FollowSerializer(serializers.ModelSerializer):
    user = PostingProfileSerializer(source='follower.userprofile', read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'user']
        read_only_fields = ('id', 'follower', 'following', 'user')

    def validate(self, attrs):
        if Follow.objects.filter(follower=self.context['request'].user,
                                 following=self.context['view'].kwargs['user_pk']).exists():
            raise serializers.ValidationError('The fields `user`, `reply` must make a unique set.',
                                              code='unique')
        return super().validate(attrs)
