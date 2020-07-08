from rest_framework import serializers

from feeds.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email')
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Photo
        fields = ['id', 'email', 'username', 'photo_images', 'photo_texts']