from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from follows.models import Follow
from profiles.serializers import PostingProfileSerializer
from users.models import User


class FollowSerializer(serializers.ModelSerializer):
    user = PostingProfileSerializer(source='follower.userprofile', read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'user']
        read_only_fields = ('id', 'follower', 'following', 'user')

    def validate(self, attrs):
        get_object_or_404(User, id=self.context['view'].kwargs.get('user_pk'))
        if Follow.objects.filter(follower=self.context['request'].user,
                                 following=self.context['view'].kwargs['user_pk']).exists():
            raise serializers.ValidationError('The fields `follower`, `following` must make a unique set.')
        elif str(self.context['request'].user.id) == self.context['view'].kwargs['user_pk']:
            raise serializers.ValidationError('Can not following yourself.')
        return super().validate(attrs)


class FollowingListSerializer(serializers.ModelSerializer):
    user = PostingProfileSerializer(source='follower.userprofile', read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'following', 'user']
        read_only_fields = ('id', 'following', 'user')


class FollowersListSerializer(serializers.ModelSerializer):
    user = PostingProfileSerializer(source='follower.userprofile', read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'user']
        read_only_fields = ('id', 'follower', 'user')
