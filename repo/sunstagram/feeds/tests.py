from django.core.files.uploadedfile import SimpleUploadedFile
from munch import Munch
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from feeds.models import Photo, PhotoFactory
from sunstagram.settings.base import MEDIA_ROOT
from users.models import User


class PhotoTestCase(APITestCase):
    def setUp(self):
        self.test_password = 1234
        self.test_user = User.objects.create(email='test@example.com',
                                             password=self.test_password,
                                             username='test')
        Token.objects.create(user_id=self.test_user.id)
        self.client.force_authenticate(user=self.test_user)
        self.image_path = MEDIA_ROOT + '/photo_images/'
        self.test_photos = PhotoFactory()
        print(self.test_photos)

    def test_should_create_photo(self):
        data = {'user': self.test_user.id,
                'photo_texts': 'for test',
                'photo_images': self.test_photos
                }
        response = self.client.post('/api/photos', data=data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        photo_response = Munch(response.data)
        self.assertTrue(photo_response.id)
        self.assertEqual(photo_response.photo_texts, data['photo_texts'])
        self.assertEqual(photo_response.photo_images, data['photo_images'])
        self.fail()
