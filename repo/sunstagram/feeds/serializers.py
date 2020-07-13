from munch import Munch
from rest_framework import serializers

from feeds.models import Post


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='user_profiles.user.username', read_only=True)
    profile_image = serializers.ImageField(source='user_profiles.profile_image', read_only=True)

    class Meta:
        model = Post
        fields = ['id',
                  'owner',
                  'profile_image',
                  'post_text',
                  'image_name',
                  'time_stamp',
                  'origin_image',
                  'thumbnail_image']
        read_only_fields = ('id',
                            'owner',
                            'profile_image',
                            'time_stamp',
                            'image_name',
                            'thumbnail_image')

    def create(self, validated_data):
        print('serializer-create!')
        print(validated_data)
        upload_image = self.context['request'].FILES

        print(upload_image)
        instance = Post.objects.create(**validated_data)

        return instance




