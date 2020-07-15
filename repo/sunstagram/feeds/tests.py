from model_bakery import baker
from munch import Munch
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from feeds.models import Post
from photos.models import PhotoFactory, Photo
from profiles.models import UserProfile, ProfileFactory
from users.models import User


class PostTestCase(APITestCase):
    def setUp(self):
        self.test_password = '1234'
        self.test_user = User.objects.create(email='test@example.com',
                                             password=self.test_password,
                                             username='test')
        self.test_post = baker.make('feeds.Post', user=self.test_user, post_text='for test')
        self.test_profile = UserProfile.objects.get(user=self.test_user)
        self.test_image = PhotoFactory().photo_images
        self.test_image2 = PhotoFactory().photo_images
        self.test_profile_image = ProfileFactory().profile_image

    def test_should_create_post(self):
        Token.objects.create(user_id=self.test_user.id)
        self.client.force_authenticate(user=self.test_user)
        data = {'post_text': 'for test'}

        response = self.client.post('/api/posts', data=data)

        post_response = Munch(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(post_response.id)
        self.assertEqual(post_response.post_text, data['post_text'])

    def test_should_create_multi_photo(self):
        Token.objects.create(user_id=self.test_user.id)
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
        Token.objects.create(user_id=self.test_user.id)
        self.client.force_authenticate(user=self.test_user)
        prev_text = self.test_post.post_text
        data = {'post_text': 'changed'}

        response = self.client.put(f'/api/posts/{self.test_post.id}', data=data)
        post_response = Munch(response.data)
        self.assertNotEqual(prev_text, post_response.post_text)

    def test_should_delete_posts(self):
        Token.objects.create(user_id=self.test_user.id)
        self.client.force_authenticate(user=self.test_user)

        response = self.client.delete(f'/api/posts/{self.test_post.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.test_post.id).exists())

    def test_should_delete_photos(self):
        Token.objects.create(user_id=self.test_user.id)
        self.client.force_authenticate(user=self.test_user)
        entry = Photo.objects.create(post=self.test_post,
                                     photo_images=self.test_image,
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
