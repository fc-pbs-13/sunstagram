from rest_framework import serializers

from feeds.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    photo_images = serializers.ListField(child=serializers.ImageField(), write_only=True)
    _images = serializers.ListField(child=serializers.ImageField(use_url=True), source='photo_images', read_only=True)

    class Meta:
        model = Photo
        fields = ['id', 'user', 'photo_images', 'photo_texts', '_images']
        read_only_fields = ('user', )
