from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'username', 'profile_image', 'web_site', 'intro', 'phone_number']

    def update(self, instance, validated_data):
        user = validated_data.pop('user')
        email = user.pop('email')
        username = user.pop('username')

        super().update(instance, validated_data)
        instance.user.email = email
        instance.user.username = username
        instance.save()
        return instance


class PostingProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'profile_image', 'following_count', 'follower_count']

