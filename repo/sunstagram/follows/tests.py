from model_bakery import baker
from munch import Munch
from rest_framework import status
from rest_framework.test import APITestCase

from follows.models import Follow
from profiles.models import UserProfile
from users.models import User


class FollowTestCase(APITestCase):
    def setUp(self):
        self.test_users = baker.make('users.User', _quantity=2)
        self.follower = self.test_users[0]
        self.following = self.test_users[1]
        self.follower_profile = UserProfile.objects.get(user_id=self.follower.id)
        self.following_profile = UserProfile.objects.get(user_id=self.following.id)
        self.expected_count = 2

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

    def test_should_list_following(self):
        test_follows = baker.make('follows.Follow', _quantity=2, following=self.following)

        response = self.client.get(f'/api/users/{self.following.id}/following')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Follow.objects.filter(following=self.following).count(), self.expected_count)

        for entry, response_entry in zip(test_follows, response.data):
            response_follower = User.objects.get(id=response_entry['id'])
            self.assertEqual(entry.follower.id, response_entry['id'])
            self.assertEqual(entry.follower.username, response_follower.username)
            self.assertEqual(response_follower.userprofile.following_count, 1)
            self.assertEqual(response_follower.userprofile.follower_count, 0)

    def test_should_list_followers(self):
        test_follows = baker.make('follows.Follow', _quantity=2, follower=self.follower)

        response = self.client.get(f'/api/users/{self.follower.id}/followers')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Follow.objects.filter(follower=self.follower).count(), self.expected_count)
        self.assertEqual(User.objects.filter(followings__follower=self.follower).count(), self.expected_count)

        for entry, response_entry in zip(test_follows, response.data):
            response_following = User.objects.get(id=response_entry['id'])
            self.assertEqual(entry.following.id, response_entry['id'])
            self.assertEqual(entry.following.username, response_following.username)
            self.assertEqual(response_following.userprofile.follower_count, 1)
            self.assertEqual(response_following.userprofile.following_count, 0)