from munch import Munch
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from profiles.models import UserProfile, ProfileFactory
from users.models import User


class UserTestCase(APITestCase):
    def setUp(self):
        self.test_password = '1234'
        self.change_password = '2345'
        self.test_user = User.objects.create(email='test@example.com',
                                             password=self.test_password,
                                             username='test')
        self.test_profile_image = ProfileFactory().profile_image

    def test_should_create_user(self):
        data = {'email': 'newemail@example.com', 'username': 'new_user', 'password': self.test_password}
        response = self.client.post('/api/users', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user_response = Munch(response.data)
        self.assertTrue(user_response.id)
        self.assertEqual(user_response.email, data['email'])
        self.assertEqual(user_response.username, data['username'])

    def test_should_login(self):
        data = {'email': 'test@example.com', 'username': 'test', 'password': self.test_password}
        response = self.client.post('/api/users/sign_in', data=data)

        user_response = Munch(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user_response.token)
        self.assertEqual(user_response.email, data['email'])
        self.assertEqual(user_response.username, data['username'])

    def test_should_logout(self):
        token = Token.objects.create(user_id=self.test_user.id)
        self.client.force_authenticate(user=self.test_user)
        response = self.client.delete('/api/users/sign_out')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Token.objects.filter(pk=token).exists())

    def test_should_delete_user(self):
        self.client.force_authenticate(user=self.test_user)
        entry = User.objects.get(id=self.test_user.id)
        response = self.client.delete(f'/api/users/{entry.id}/deactivate')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(id=entry.id).exists())

    def test_should_change_password(self):
        entry = User.objects.get(id=self.test_user.id)
        Token.objects.create(user_id=self.test_user.id)
        self.client.force_authenticate(user=self.test_user)
        data = {'password': self.test_password,
                'new_password': self.change_password,
                'new_password2': self.change_password}

        response = self.client.patch(f'/api/users/{entry.id}/change_password', data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_should_update_userprofile(self):
        entry = UserProfile.objects.get(user_id=self.test_user.id)
        Token.objects.create(user_id=self.test_user.id)
        self.client.force_authenticate(user=self.test_user)

        data = {'email': 'changed@example.com',
                'username': 'changed',
                'web_site': 'https://www.google.com',
                'profile_image': self.test_profile_image,
                'intro': 'test intro',
                'phone_number': '010-1234-5678'}
        response = self.client.put(f'/api/profile/{entry.id}', data=data, format='multipart')

        user_response = Munch(response.data)
        self.assertEqual(user_response.email, data['email'])
        self.assertEqual(user_response.username, data['username'])
        self.assertEqual(user_response.web_site, data['web_site'])
        self.assertEqual(user_response.intro, data['intro'])
        self.assertEqual(user_response.phone_number, data['phone_number'])
        self.assertEqual(user_response.profile_image, 'http://testserver/profile_images/example.jpg')
