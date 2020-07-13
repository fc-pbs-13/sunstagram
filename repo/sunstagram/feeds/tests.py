from django.test.client import encode_multipart, BOUNDARY, MULTIPART_CONTENT
from munch import Munch
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from feeds.models import PostFactory
from profiles.models import UserProfile, ProfileFactory
from users.models import User


class PhotoTestCase(APITestCase):
    def setUp(self):
        self.test_password = '1234'
        self.test_user = User.objects.create(email='test@example.com',
                                             password=self.test_password,
                                             username='test')
        self.test_profile = UserProfile.objects.get(user=self.test_user)
        self.test_image = PostFactory().origin_image
        self.test_profile_image = ProfileFactory().profile_image

    def test_should_create_post(self):
        Token.objects.create(user_id=self.test_user.id)
        self.client.force_authenticate(user=self.test_user)
        data = {'post_text': 'for test',
                'origin_image': self.test_image}

        response = self.client.post('/api/posts', data=data, format='multipart')

        photo_response = Munch(response.data)
        print(photo_response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(photo_response.id)
        self.assertEqual(photo_response.photo_texts, data['post_text'])
        self.assertEqual(photo_response.photo_images, data['origin_images'])
        self.fail()
