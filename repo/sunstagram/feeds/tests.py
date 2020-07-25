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
        self.test_password = '1234'
        self.test_user = User.objects.create(email='test@example.com',
                                             password=self.test_password,
                                             username='test')
        self.test_post = baker.make('feeds.Post', user=self.test_user)
        self.test_profile = UserProfile.objects.get(user=self.test_user)
        self.test_image = ImageMaker.temporary_image()
        self.test_image2 = ImageMaker.temporary_image()
        self.test_profile_image = ProfileFactory().profile_image
        self.expected_tag_count = 2

    def test_should_create_post_with_hash_tag(self):
        self.client.force_authenticate(user=self.test_user)
        data = {'post_text': 'for test', 'tag': {'name': ['cat', 'dog']}}

        response = self.client.post('/api/posts', data=data)

        post_response = Munch(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(post_response.id)
        self.assertEqual(post_response.post_text, data['post_text'])
        # tag 생성 검사
        for name in data['tag']['name']:
            self.assertTrue(HashTag.objects.filter(name=name).exists())
        self.assertEqual(TagPostList.objects.filter(post_id=post_response.id).count(),
                         self.expected_tag_count)

    def test_should_create_post_no_tag(self):
        self.client.force_authenticate(user=self.test_user)
        data = {'post_text': 'for test'}

        response = self.client.post('/api/posts', data=data)

        post_response = Munch(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(post_response.id)
        self.assertEqual(post_response.post_text, data['post_text'])

    def test_should_create_multi_photo(self):
        self.client.force_authenticate(user=self.test_user)
        data = {'photo_images': [self.test_image, self.test_image2],
                'post_id': self.test_post.id}

        response = self.client.post(f'/api/posts/{self.test_post.id}/photos', data=data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Photo.objects.filter(post=self.test_post).count(), 2)

    def test_should_list_posts(self):
        posts = baker.make('feeds.Post', user=self.test_user, _quantity=2)
        response = self.client.get('/api/posts')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for test_post, post_response in zip(posts[::-1], response.data):
            self.assertEqual(test_post.id, post_response['id'])
            self.assertEqual(test_post.post_text, post_response['post_text'])

    def test_should_update_posts(self):
        self.client.force_authenticate(user=self.test_user)
        prev_text = self.test_post.post_text
        data = {'post_text': 'changed'}

        response = self.client.put(f'/api/posts/{self.test_post.id}', data=data)
        post_response = Munch(response.data)
        self.assertNotEqual(prev_text, post_response.post_text)

    def test_should_update_posts_with_tag(self):
        self.client.force_authenticate(user=self.test_user)
        test_tag = HashTag.objects.create(name='test')
        TagPostList.objects.create(post=self.test_post, tag=test_tag)
        prev_text = self.test_post.post_text
        data = {'post_text': 'changed', 'tag': {'name': ['test', 'python']}}

        response = self.client.put(f'/api/posts/{self.test_post.id}', data=data)
        post_response = Munch(response.data)
        self.assertNotEqual(prev_text, post_response.post_text)
        # tag 업데이트 검사 ( before: 'test' -> after: 'test', 'python')
        for name in data['tag']['name']:
            self.assertTrue(HashTag.objects.filter(name=name).exists())
        self.assertEqual(TagPostList.objects.filter(post_id=post_response.id).count(),
                         self.expected_tag_count)

    def test_should_delete_posts(self):
        self.client.force_authenticate(user=self.test_user)

        response = self.client.delete(f'/api/posts/{self.test_post.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.test_post.id).exists())

    def test_should_delete_photos(self):
        self.client.force_authenticate(user=self.test_user)
        entry = Photo.objects.create(post=self.test_post,
                                     photo_images=self.test_image.name,
                                     image_name=self.test_image.name,
                                     user=self.test_user)

        response = self.client.delete(f'/api/photos/{entry.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Photo.objects.filter(id=self.test_post.id).exists())

    # def test_should_update_photo(self):
    #     """
    #     Issue : UTF-8 codec can't decode byte 0xff in position 0
    #     """
    #     Token.objects.create(user_id=self.test_user.id)
    #     self.client.force_authenticate(user=self.test_user)
    #     prev_photo = self.test_image
    #     photo = Photo.objects.create(post=self.test_post,
    #                                  photo_images=self.test_image,
    #                                  user=self.test_user)
    #     data = {'photo_images': self.test_image2,
    #             'post_id': self.test_post.id}
    #
    #     response = self.client.put(f'/api/posts/{self.test_post.id}/photos/{photo.id}', data=data)
    #     photo_response = Munch(response.data)
    #     self.assertNotEqual(prev_photo, photo_response.photo_images)
    #     self.fail()
    #
    # def test_should_retrieve_photos(self):
    #     """
    #     Issue : UTF-8 codec can't decode byte 0xff in position 0
    #     """
    #     photo = Photo.objects.create(post=self.test_post,
    #                                  photo_images=self.test_image,
    #                                  image_name=self.test_image.name,
    #                                  user=self.test_user)
    #
    #     response = self.client.get(f'/api/posts/{self.test_post.id}/photos/{photo.id}')
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.fail()

