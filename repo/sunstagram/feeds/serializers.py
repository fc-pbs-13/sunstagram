from rest_framework import serializers

from feeds.models import Post, HashTag, TagPostList
from photos.serializers import PhotoSerializer


class HashTagSerializer(serializers.ModelSerializer):
    name = serializers.ListField(child=serializers.CharField(max_length=12), write_only=True)

    class Meta:
        model = HashTag
        fields = ['id', 'name', 'tag_count']
        read_only_fields = ('id', 'tag_count')


class TagShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TagPostList
        fields = ['id', 'post', 'tag']
        read_only_fields = ('id', 'post', 'tag')


class PostWithTagSerializer(serializers.ModelSerializer):
    images = PhotoSerializer(many=True, read_only=True)
    tag = HashTagSerializer(write_only=True)
    profile_image = serializers.ImageField(source='userprofile.profile_image', read_only=True)

    class Meta:
        model = Post
        fields = ['id',
                  'profile_image',
                  'post_text',
                  'time_stamp',
                  'images',
                  'like_count',
                  'tag']
        read_only_fields = ('id',
                            'profile_image',
                            'time_stamp',
                            'images',
                            'like_count',
                            )

    def create(self, validated_data):
        obj_id_list = []

        for name in validated_data['tag']['name']:
            obj, _ = HashTag.objects.update_or_create(name=name)
            obj_id_list.append(obj.id)

        validated_data.pop('tag')
        post = Post.objects.create(**validated_data)

        data = {'post': post.id, 'tag': {*obj_id_list}}
        # validate unique-together
        serializer = TagPostListSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        for obj_id in obj_id_list:
            tag = HashTag.objects.get(id=obj_id)
            TagPostList.objects.create(post=post, tag=tag)
        return post

    def update(self, instance, validated_data):
        obj_id_list = []

        for name in validated_data['tag']['name']:
            obj, _ = HashTag.objects.update_or_create(name=name)
            obj_id_list.append(obj.id)

        validated_data.pop('tag')

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for obj_id in obj_id_list:
            tag = HashTag.objects.get(id=obj_id)
            TagPostList.objects.get_or_create(post=instance, tag=tag)

        return instance


class PostSerializer(serializers.ModelSerializer):
    images = PhotoSerializer(many=True, read_only=True)
    profile_image = serializers.ImageField(source='userprofile.profile_image', read_only=True)

    class Meta:
        model = Post
        fields = ['id',
                  'profile_image',
                  'post_text',
                  'time_stamp',
                  'images',
                  'like_count']
        read_only_fields = ('id',
                            'profile_image',
                            'time_stamp',
                            'images',
                            'like_count',
                            )


class TagPostListSerializer(serializers.ModelSerializer):
    tag = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        model = TagPostList
        fields = ['id', 'post', 'tag']
        read_only_fields = ('id',)

    def validate(self, attrs):
        for tag_id in attrs['tag']:
            if TagPostList.objects.filter(post=attrs['post'], tag=tag_id).exists():
                raise serializers.ValidationError('The fields `post`, `tag` must make a unique set.')
        return attrs
