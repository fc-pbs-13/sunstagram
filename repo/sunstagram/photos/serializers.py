from rest_framework import serializers

from feeds.models import Post
from photos.models import Photo


class PhotoSerializer(serializers.ModelSerializer):
    photos = serializers.ListField(child=serializers.ImageField(), write_only=True)

    class Meta:
        model = Photo
        fields = ['id', 'photo_images', 'user', 'photos']
        read_only_fields = ('id', 'image_name', 'photo_images', 'user')

    def create(self, validated_data):
        post = Post.objects.get(id=self.context['request'].data['post_id'])
        images_data = self.context['request'].FILES
        photo_bulk_list = []

        for image in images_data.getlist('photos'):
            photo = Photo(post=post,
                          photo_images=image,
                          image_name=image.name,
                          user=self.context['request'].user)
            photo_bulk_list.append(photo)
        Photo.objects.bulk_create(photo_bulk_list)

        return post


