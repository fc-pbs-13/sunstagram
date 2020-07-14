from rest_framework import serializers

from feeds.models import Post
from photos.serializers import PhotoSerializer


class PostSerializer(serializers.ModelSerializer):
    images = PhotoSerializer(many=True, read_only=True)
    owner = serializers.CharField(source='user', read_only=True)
    profile_image = serializers.ImageField(source='userprofile.profile_image', read_only=True)

    class Meta:
        model = Post
        fields = ['id',
                  'owner',
                  'profile_image',
                  'post_text',
                  'time_stamp',
                  'images']
        read_only_fields = ('id',
                            'owner',
                            'profile_image',
                            'time_stamp',
                            'images')




