from model_bakery import baker
from munch import Munch
from rest_framework import status
from rest_framework.test import APITestCase

from feeds.models import Post
from likes.models import PostLike


class PostTestCase(APITestCase):
    def setUp(self):
        self.test_users = baker.make('users.User', _quantity=2)
        self.test_posts = baker.make('feeds.Post', user=self.test_users[0], _quantity=2)

    def test_should_create_post_like(self):
        user = self.test_users[0]
        self.client.force_authenticate(user=user)
        response = self.client.post(f'/api/posts/{self.test_posts[0].id}/post_likes')

        like_response = Munch(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(like_response.id)
        self.assertEqual(Post.objects.get(id=like_response.post).like_count, 1)
        self.assertEqual(like_response.user['id'], user.id)
        self.assertEqual(like_response.user['username'], user.username)
        self.assertEqual(like_response.user['profile_image'], 'http://testserver/profile_images/default.jpg')

    def test_should_not_duplicate(self):
        user = self.test_users[0]
        self.client.force_authenticate(user=user)
        PostLike.objects.create(post=self.test_posts[0], user=user)

        #Key (user_id, post_id)=(1, 1) already exists.
        response = self.client.post(f'/api/posts/{self.test_posts[0].id}/post_likes')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_create_another_post_like(self):
        user = self.test_users[0]
        self.client.force_authenticate(user=user)
        PostLike.objects.create(post=self.test_posts[0], user=user)
        response = self.client.post(f'/api/posts/{self.test_posts[1].id}/post_likes')

        like_response = Munch(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(like_response.id)
        self.assertEqual(Post.objects.get(id=like_response.post).like_count, 1)

    def test_should_list_post_likes(self):
        PostLike.objects.create(post=self.test_posts[0], user=self.test_users[0])
        PostLike.objects.create(post=self.test_posts[0], user=self.test_users[1])
        response = self.client.get(f'/api/posts/{self.test_posts[0].id}/post_likes')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)

    def test_should_delete_post_like(self):
        user = self.test_users[0]
        self.client.force_authenticate(user=user)
        entry = PostLike.objects.create(post=self.test_posts[0], user=user)

        response = self.client.delete(f'/api/post_likes/{entry.id}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=entry.id).exists())
        self.assertEqual(Post.objects.get(id=self.test_posts[0].id).like_count, 0)
