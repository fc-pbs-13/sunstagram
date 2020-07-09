from django.core.files.uploadedfile import SimpleUploadedFile
from munch import Munch
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from sunstagram.settings.base import MEDIA_ROOT
from users.models import User


class PhotoTestCase(APITestCase):
    def setUp(self):
        self.test_password = 1234
        self.test_user = User.objects.create(email='test@example.com',
                                             password=self.test_password,
                                             username='test')

    def test_should_create_photo(self):
        Token.objects.create(user_id=self.test_user.id)
        self.client.force_authenticate(user=self.test_user)
        image_path = MEDIA_ROOT + '/photo_images/testimage.png'
        test_image = SimpleUploadedFile(name='testimage.png',
                                        content=open(image_path, 'rb').read(),
                                        content_type='image/png')

        data = {'user': self.test_user.id,
                'photo_texts': 'for test',
                'photo_images': test_image
        }
        response = self.client.post('/api/photos', data=data, content_type='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        photo_response = Munch(response.data)
        self.assertTrue(photo_response.id)
        self.assertEqual(photo_response.photo_texts, data['photo_texts'])
        # self.assertEqual(photo_response.photo_images, data['photo_images'])
