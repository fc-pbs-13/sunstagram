from munch import Munch
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from accounts.models import Account


class UserTestCase(APITestCase):
    def setUp(self) -> None:
        self.testAccount = Account.objects.create(email="test@example.com", username="test", password="1111", )
        self.data = {"email": self.testAccount.email, "username": "test", "password": "1111", }
        self.testAccount.set_password(self.testAccount.password)
        self.testAccount.save()

    def test_should_create(self):
        data = {"email": "newemail@example.com", "username": "newuser", "password": "1111"}
        response = self.client.post('/api/users/sign_up', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user_response = Munch(response.data)
        print(user_response)
        print("user created result")
        self.assertTrue(user_response.id)
        self.assertEqual(user_response.email, data['email'])
        self.assertEqual(user_response.username, data['username'])

    def test_should_login(self):
        response = self.client.post('/api/users/sign_in', data=self.data)
        user_response = Munch(response.data)
        print(user_response)
        print("login result")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user_response.token)
        self.assertEqual(user_response.email, self.data['email'])
        self.assertEqual(user_response.username, self.data['username'])

    def test_should_logout(self):
        response = self.client.post('/api/users/sign_in', data=self.data)
        token = response.data['token']
        self.client.force_authenticate(user=self.testAccount, token=token)
        response = self.client.delete('/api/users/sign_out')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Token.objects.filter(pk=token).exists())

    def test_should_delete_account(self):
        self.client.force_authenticate(user=self.testAccount)
        entry = Account.objects.get(id=self.testAccount.id)
        response = self.client.delete(f'/api/users/{entry.id}/deactivate')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Account.objects.filter(id=entry.id).exists())


