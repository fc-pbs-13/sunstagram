from model_bakery import baker
from munch import Munch
from rest_framework import status
from rest_framework.test import APITestCase

from feeds.models import Post, TagPostList, HashTag
from photos.models import Photo
from profiles.models import UserProfile, ProfileFactory
from stories.models import ImageMaker
from users.models import User


class PostTestCase(APITestCase):
    def setUp(self):
        self.test_users = baker.make('users.User', _quantity=2)
        self.test_post = baker.make('feeds.Post', user=self.test_users[0])
        self.test_image = ImageMaker.temporary_image()
        self.test_image2 = ImageMaker.temporary_image(name='test2.jpg')
        self.expected_tag_count = 2

    def test_should_create_post_with_hash_tag(self):
        self.client.force_authenticate(user=self.test_users[0])
        data = {'post_text': 'for test', 'tags': ['cat', 'dog']}

        response = self.client.post('/api/posts', data=data)

        post_response = Munch(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(post_response.id)
        self.assertEqual(post_response.post_text, data['post_text'])
        # tag 생성 검사
        for name in data['tags']:
            self.assertTrue(HashTag.objects.filter(name=name).exists())
        self.assertEqual(TagPostList.objects.filter(post_id=post_response.id).count(),
                         self.expected_tag_count)

    def test_should_create_multi_photo(self):
        expected_photos_count = 2
        self.client.force_authenticate(user=self.test_users[0])
        data = {'photos': [self.test_image, self.test_image2],
                'post_id': self.test_post.id}

        response = self.client.post(f'/api/posts/{self.test_post.id}/photos', data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Photo.objects.filter(post=self.test_post).count(), expected_photos_count)

    def test_should_list_posts(self):
        # setUp - self.test_post 포함 3개의 post가 list 되어야 함
        expected_post_count = 3
        posts = baker.make('feeds.Post', user=self.test_users[1], _quantity=2)
        profile = UserProfile.objects.get(user=self.test_users[1])
        test_tag = baker.make('feeds.HashTag', name='test')
        for i in range(2):
            baker.make('photos.Photo', user=self.test_users[1], post=posts[i], photo_images=self.test_image.name)
            baker.make('feeds.TagPostList', post=posts[i], tag=test_tag)

        response = self.client.get('/api/posts')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.all().count(), expected_post_count)

        for test_post, post_response in zip(posts[::-1], response.data):
            self.assertEqual(test_post.id, post_response['id'])
            self.assertEqual(test_post.post_text, post_response['post_text'])

            self.assertEqual(test_tag.id, post_response['_tags'][0]['tag']['id'])
            self.assertEqual(test_tag.name, post_response['_tags'][0]['tag']['name'])

            self.assertEqual(profile.user.id, post_response['user']['id'])
            self.assertEqual(profile.user.username, post_response['user']['username'])
            self.assertTrue('.jpg' in post_response['user']['profile_image'])

            self.assertEqual(HashTag.objects.get(id=test_tag.id).tag_count,
                             post_response['_tags'][0]['tag']['tag_count'])
            self.assertTrue('.jpg' in post_response['images'][0]['photo_images'])

    def test_should_list_tags_from_search(self):
        expected_count = 2
        self.client.force_authenticate(user=self.test_users[0])
        HashTag.objects.create(name='cat')
        HashTag.objects.create(name='car')
        HashTag.objects.create(name='dog')
        response = self.client.get('/api/tags?keyword=c')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(HashTag.objects.filter(name__startswith='c').count(), expected_count)

    def test_should_list_tagged_posts_from_search(self):
        expected_count = 2
        self.client.force_authenticate(user=self.test_users[1])
        tag = HashTag.objects.create(name='cat')
        posts = baker.make('feeds.Post', user=self.test_users[1], _quantity=2)
        for i in range(2):
            baker.make('feeds.TagPostList', post=posts[i], tag=tag)

        response = self.client.get(f'/api/tags/{tag.id}/posts')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.filter(tagged_posts__tag=tag).count(), expected_count)
        for res in response.data:
            self.assertEqual(res['_tags'][0]['tag']['name'], tag.name)

    def test_should_update_posts_with_tag(self):
        self.client.force_authenticate(user=self.test_users[0])

        test_tag = HashTag.objects.create(name='test')
        TagPostList.objects.create(post=self.test_post, tag=test_tag)
        prev_text = self.test_post.post_text
        data = {'post_text': 'changed', 'tags': ['test', 'python']}

        response = self.client.put(f'/api/posts/{self.test_post.id}', data=data)
        post_response = Munch(response.data)
        self.assertNotEqual(prev_text, post_response.post_text)
        # tag 업데이트 검사 ( before: 'test' -> after: 'test', 'python')
        for name in data['tags']:
            self.assertTrue(HashTag.objects.filter(name=name).exists())
        self.assertEqual(TagPostList.objects.filter(post_id=post_response.id).count(),
                         self.expected_tag_count)

    def test_should_delete_posts(self):
        self.client.force_authenticate(user=self.test_users[0])

        response = self.client.delete(f'/api/posts/{self.test_post.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.test_post.id).exists())

    def test_should_delete_tag_post(self):
        self.client.force_authenticate(user=self.test_users[0])
        test_tag = baker.make('feeds.HashTag', name='abc')
        entry = baker.make('feeds.TagPostList', post=self.test_post, tag=test_tag)

        response = self.client.delete(f'/api/posts/{self.test_post.id}/tags/{entry.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(TagPostList.objects.filter(id=entry.id).exists())

    def test_should_delete_photos(self):
        self.client.force_authenticate(user=self.test_users[0])
        entry = Photo.objects.create(post=self.test_post,
                                     photo_images=self.test_image.name,
                                     image_name=self.test_image.name,
                                     user=self.test_users[0])

        response = self.client.delete(f'/api/photos/{entry.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Photo.objects.filter(id=self.test_post.id).exists())

    def test_should_update_photo(self):
        self.client.force_authenticate(user=self.test_users[0])
        prev_photo = self.test_image
        photo = Photo.objects.create(post=self.test_post,
                                     photo_images=prev_photo.name,
                                     user=self.test_users[0])
        data = {'photos': [self.test_image2],
                'post_id': self.test_post.id}

        response = self.client.put(f'/api/posts/{self.test_post.id}/photos/{photo.id}', data=data,
                                   format='multipart')
        photo_response = Munch(response.data)
        self.assertNotEqual(prev_photo, photo_response.photo_images)

    def test_should_retrieve_photos(self):
        photo = Photo.objects.create(post=self.test_post,
                                     photo_images=self.test_image.name,
                                     image_name=self.test_image.name,
                                     user=self.test_users[0])

        response = self.client.get(f'/api/posts/{self.test_post.id}/photos/{photo.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(photo.id, response.data['id'])
        self.assertTrue('.jpg' in response.data['photo_images'])
