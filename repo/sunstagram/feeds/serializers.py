from rest_framework import serializers

from feeds.models import Post, HashTag, TagPostList
from photos.serializers import PhotoSerializer
from profiles.serializers import PostingProfileSerializer


class HashTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = HashTag
        fields = ['id', 'name', 'tag_count']
        read_only_fields = ('id', 'name', 'tag_count')


class TagShowSerializer(serializers.ModelSerializer):
    tag = HashTagSerializer()

    class Meta:
        model = TagPostList
        fields = ['id', 'post', 'tag']
        read_only_fields = ('id', 'post', 'tag')


class PostSerializer(serializers.ModelSerializer):
    images = PhotoSerializer(many=True, read_only=True, source='photo_posts')
    tags = serializers.ListField(child=serializers.CharField(max_length=12), write_only=True)
    _tags = TagShowSerializer(many=True, read_only=True, source='tagged_posts')
    user = PostingProfileSerializer(source='user.userprofile', read_only=True)

    class Meta:
        model = Post
        fields = ['id',
                  'post_text',
                  'time_stamp',
                  'images',
                  'like_count',
                  'tags',
                  '_tags',
                  'user']
        read_only_fields = ('id',
                            'time_stamp',
                            'images',
                            'like_count',
                            'user'
                            )

    def create(self, validated_data):
        if validated_data.get('tags'):
            obj_id_list = []

            for name in validated_data['tags']:
                obj, _ = HashTag.objects.update_or_create(name=name)
                obj_id_list.append(obj.id)

            validated_data.pop('tags')
            post = Post.objects.create(**validated_data)

            data = {'post': post.id, 'tag': {*obj_id_list}}
            # validate unique-together
            serializer = TagPostListSerializer(data=data)
            serializer.is_valid(raise_exception=True)

            for obj_id in obj_id_list:
                tag = HashTag.objects.get(id=obj_id)
                TagPostList.objects.create(post=post, tag=tag)
        else:
            post = Post.objects.create(**validated_data)
        return post

    def update(self, instance, validated_data):
        if validated_data.get('tags'):
            obj_id_list = []

            for name in validated_data['tags']:
                obj, _ = HashTag.objects.update_or_create(name=name)
                obj_id_list.append(obj.id)

            validated_data.pop('tags')

            for obj_id in obj_id_list:
                tag = HashTag.objects.get(id=obj_id)
                TagPostList.objects.get_or_create(post=instance, tag=tag)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


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
