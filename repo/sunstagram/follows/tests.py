from model_bakery import baker
from munch import Munch
from rest_framework import status
from rest_framework.test import APITestCase

from follows.models import Follow
from profiles.models import UserProfile


class FollowTestCase(APITestCase):
    def setUp(self):
        self.test_users = baker.make('users.User', _quantity=3)
        self.follower = self.test_users[0]
        self.following = self.test_users[1]
        self.follower_profile = UserProfile.objects.get(user_id=self.follower.id)
        self.following_profile = UserProfile.objects.get(user_id=self.following.id)

    def test_should_create_following(self):
        self.client.force_authenticate(user=self.follower)
        response = self.client.post(f'/api/users/{self.following.id}/follows')

        follow_response = Munch(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(follow_response.id)
        self.assertEqual(follow_response.follower, self.follower.id)
        self.assertEqual(follow_response.following, self.following.id)
        self.assertEqual(follow_response.user['id'], self.follower.id)
        self.assertEqual(follow_response.user['username'], self.follower.username)
        self.assertEqual(follow_response.user['profile_image'], 'http://testserver/profile_images/default.jpg')
        self.assertEqual(UserProfile.objects.get(user_id=self.follower.id).following_count, 1)
        self.assertEqual(UserProfile.objects.get(user_id=self.follower.id).follower_count, 0)
        self.assertEqual(UserProfile.objects.get(user_id=self.following.id).following_count, 0)
        self.assertEqual(UserProfile.objects.get(user_id=self.following.id).follower_count, 1)

    def test_should_not_duplicate_following(self):
        self.client.force_authenticate(user=self.follower)
        Follow.objects.create(follower=self.follower, following=self.following)
        response = self.client.post(f'/api/users/{self.following.id}/follows')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_delete_follow(self):
        self.client.force_authenticate(user=self.follower)
        entry = Follow.objects.create(follower=self.follower, following=self.following)

        response = self.client.delete(f'/api/follows/{entry.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertFalse(Follow.objects.filter(id=entry.id).exists())
        self.assertEqual(UserProfile.objects.get(user_id=self.follower.id).following_count, 0)
        self.assertEqual(UserProfile.objects.get(user_id=self.following.id).follower_count, 0)

    def test_should_list_follow(self):
        new_follower = self.test_users[2]
        entry_1 = Follow.objects.create(follower=self.follower, following=self.following)
        entry_2 = Follow.objects.create(follower=new_follower, following=self.following)

        response = self.client.get(f'/api/users/{self.following.id}/follows')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data[0]['user']['id'], self.follower.id)
        self.assertEqual(response.data[0]['user']['username'], self.follower.username)
        self.assertEqual(response.data[0]['user']['profile_image'], 'http://testserver/profile_images/default.jpg')

        self.assertEqual(entry_1.id, response.data[0]['id'])
        self.assertEqual(entry_1.follower.id, response.data[0]['follower'])
        self.assertEqual(entry_1.following.id, response.data[0]['following'])
        self.assertEqual(UserProfile.objects.get(user_id=self.follower.id).following_count, 1)

        self.assertEqual(entry_2.id, response.data[1]['id'])
        self.assertEqual(entry_2.follower.id, response.data[1]['follower'])
        self.assertEqual(entry_2.following.id, response.data[1]['following'])
        self.assertEqual(UserProfile.objects.get(user_id=new_follower.id).following_count, 1)

        self.assertEqual(UserProfile.objects.get(user_id=self.following.id).follower_count, 2)
