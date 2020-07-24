from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from feeds.models import Post, HashTag, TagPostList
from photos.serializers import PhotoSerializer


class HashTagSerializer(serializers.ModelSerializer):
    name = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model = HashTag
        fields = ['id', 'name', 'tag_count']
        read_only_fields = ('id', 'tag_count')

    # def validate(self, attrs):
    #     print('here')
    #     if not Post.objects.filter(id=self.context['request'].data.get('post'),
    #                                user=self.context['request'].user.id).exists():
    #         raise serializers.ValidationError('post does not exists')
    #     for name in attrs['name']:
    #         if HashTag.objects.filter(name=name).exists():
    #             attrs['name'].remove(name)
    #     return attrs


class PostSerializer(serializers.ModelSerializer):
    images = PhotoSerializer(many=True, read_only=True)
    tag = HashTagSerializer(many=True)
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
                            'like_count')

    def create(self, validated_data):
        obj_id_list = []
        for name in validated_data['tag'][0]['name']:
            obj, _ = HashTag.objects.get_or_create(name=name)
            obj_id_list.append(obj.id)

        validated_data.pop('tag')
        post = Post.objects.create(**validated_data)

        data = {'post': post.id, 'tag': {*obj_id_list}}
        # validate unique-together
        serializer = TagPostListSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        for obj_id in obj_id_list:
            print(HashTag.objects.get(id=obj_id).id)
            tag = HashTag.objects.get(id=obj_id)
            TagPostList.objects.create(post=post, tag=tag)
        return post


class TagPostListSerializer(serializers.ModelSerializer):
    tag = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = TagPostList
        fields = ['id', 'post', 'tag']
        read_only_fields = ('id', )

    def validate(self, attrs):
        for tag_id in attrs['tag']:
            if TagPostList.objects.filter(post=attrs['post'], tag=tag_id).exists():
                raise serializers.ValidationError('The fields `post`, `tag` must make a unique set.')
        return attrs




