from model_bakery import baker
from munch import Munch
from rest_framework import status
from rest_framework.test import APITestCase

from comments.models import Comment
from feeds.models import Post
from likes.models import PostLike, CommentLike, ReplyLike
from replies.models import Reply


class LikesTestCase(APITestCase):
    def setUp(self):
        self.test_users = baker.make('users.User', _quantity=2)
        self.test_user = self.test_users[0]
        self.test_posts = baker.make('feeds.Post', user=self.test_users[0], _quantity=2)
        self.test_comments = baker.make('comments.Comment',
                                        user=self.test_users[0],
                                        post=self.test_posts[0],
                                        _quantity=2)
        self.test_replies = baker.make('replies.Reply',
                                       user=self.test_users[0],
                                       comment=self.test_comments[0],
                                       _quantity=2)

    def test_should_create_post_like(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(f'/api/posts/{self.test_posts[0].id}/post_likes')

        like_response = Munch(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(like_response.id)
        self.assertEqual(Post.objects.get(id=like_response.post).like_count, 1)
        self.assertEqual(like_response.user['id'], self.test_user.id)
        self.assertEqual(like_response.user['username'], self.test_user.username)
        self.assertEqual(like_response.user['profile_image'], 'http://testserver/profile_images/default.jpg')

    def test_should_not_duplicate(self):
        self.client.force_authenticate(user=self.test_user)
        PostLike.objects.create(post=self.test_posts[0], user=self.test_user)

        response = self.client.post(f'/api/posts/{self.test_posts[0].id}/post_likes')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_create_another_post_like(self):
        self.client.force_authenticate(user=self.test_user)
        PostLike.objects.create(post=self.test_posts[0], user=self.test_user)
        response = self.client.post(f'/api/posts/{self.test_posts[1].id}/post_likes')

        like_response = Munch(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(like_response.id)
        self.assertEqual(Post.objects.get(id=like_response.post).like_count, 1)

    def test_should_list_post_likes(self):
        like_1 = PostLike.objects.create(post=self.test_posts[0], user=self.test_users[0])
        like_2 = PostLike.objects.create(post=self.test_posts[0], user=self.test_users[1])
        response = self.client.get(f'/api/posts/{self.test_posts[0].id}/post_likes')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(like_2.id, response.data[0]['id'])
        self.assertEqual(like_2.user_id, response.data[0]['user']['id'])
        self.assertEqual(like_2.user.username, response.data[0]['user']['username'])
        self.assertEqual(like_1.id, response.data[1]['id'])
        self.assertEqual(like_1.user_id, response.data[1]['user']['id'])
        self.assertEqual(like_1.user.username, response.data[1]['user']['username'])

    def test_should_delete_post_like(self):
        self.client.force_authenticate(user=self.test_user)
        entry = PostLike.objects.create(post=self.test_posts[0], user=self.test_user)

        response = self.client.delete(f'/api/post_likes/{entry.id}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=entry.id).exists())
        self.assertEqual(Post.objects.get(id=self.test_posts[0].id).like_count, 0)

    def test_should_create_comment_like(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(f'/api/comments/{self.test_comments[0].id}/comment_likes')

        like_response = Munch(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(like_response.id)
        self.assertEqual(Comment.objects.get(id=like_response.comment).like_count, 1)
        self.assertEqual(like_response.user['id'], self.test_user.id)
        self.assertEqual(like_response.user['username'], self.test_user.username)
        self.assertEqual(like_response.user['profile_image'], 'http://testserver/profile_images/default.jpg')

    def test_should_not_duplicate_comment_likes(self):
        self.client.force_authenticate(user=self.test_user)
        CommentLike.objects.create(comment=self.test_comments[0], user=self.test_user)

        response = self.client.post(f'/api/comments/{self.test_comments[0].id}/comment_likes')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_create_another_comment_like(self):
        self.client.force_authenticate(user=self.test_user)
        CommentLike.objects.create(comment=self.test_comments[0], user=self.test_user)
        response = self.client.post(f'/api/comments/{self.test_comments[1].id}/comment_likes')

        like_response = Munch(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(like_response.id)
        self.assertEqual(Comment.objects.get(id=like_response.comment).like_count, 1)

    def test_should_list_comment_likes(self):
        like_1 = CommentLike.objects.create(comment=self.test_comments[0], user=self.test_users[0])
        like_2 = CommentLike.objects.create(comment=self.test_comments[0], user=self.test_users[1])
        response = self.client.get(f'/api/comments/{self.test_comments[0].id}/comment_likes')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(like_2.id, response.data[0]['id'])
        self.assertEqual(like_2.user_id, response.data[0]['user']['id'])
        self.assertEqual(like_2.user.username, response.data[0]['user']['username'])
        self.assertEqual(like_1.id, response.data[1]['id'])
        self.assertEqual(like_1.user_id, response.data[1]['user']['id'])
        self.assertEqual(like_1.user.username, response.data[1]['user']['username'])

    def test_should_delete_comment_like(self):
        self.client.force_authenticate(user=self.test_user)
        entry = CommentLike.objects.create(comment=self.test_comments[0], user=self.test_user)

        response = self.client.delete(f'/api/comment_likes/{entry.id}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(id=entry.id).exists())
        self.assertEqual(Comment.objects.get(id=self.test_comments[0].id).like_count, 0)

    def test_should_create_reply_like(self):
        self.client.force_authenticate(user=self.test_user)
        entry = Reply.objects.create(user=self.test_user,
                                     comment=self.test_comments[0],
                                     reply_text='for test')
        response = self.client.post(
            f'/api/posts/{self.test_posts[0].id}/'
            f'comments/{self.test_comments[0].id}/'
            f'replies/{entry.id}/reply_likes')

        like_response = Munch(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.data)
        self.assertTrue(like_response.id)
        self.assertEqual(Reply.objects.get(id=like_response.reply).like_count, 1)
        self.assertEqual(like_response.user['id'], self.test_user.id)
        self.assertEqual(like_response.user['username'], self.test_user.username)
        self.assertEqual(like_response.user['profile_image'], 'http://testserver/profile_images/default.jpg')

    def test_should_not_duplicate_reply_likes(self):
        self.client.force_authenticate(user=self.test_user)
        ReplyLike.objects.create(reply=self.test_replies[0], user=self.test_user)

        response = self.client.post(
            f'/api/posts/{self.test_posts[0].id}/'
            f'comments/{self.test_comments[0].id}/'
            f'replies/{self.test_replies[0].id}/reply_likes')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_create_another_reply_like(self):
        self.client.force_authenticate(user=self.test_user)
        ReplyLike.objects.create(reply=self.test_replies[0], user=self.test_user)
        response = self.client.post(
            f'/api/posts/{self.test_posts[0].id}/'
            f'comments/{self.test_comments[0].id}/'
            f'replies/{self.test_replies[1].id}/reply_likes')

        like_response = Munch(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(like_response.id)
        self.assertEqual(Reply.objects.get(id=like_response.reply).like_count, 1)

    def test_should_list_reply_likes(self):
        like_1 = ReplyLike.objects.create(reply=self.test_replies[0], user=self.test_users[0])
        like_2 = ReplyLike.objects.create(reply=self.test_replies[0], user=self.test_users[1])
        response = self.client.get(
            f'/api/posts/{self.test_posts[0].id}/'
            f'comments/{self.test_comments[0].id}/'
            f'replies/{self.test_replies[0].id}/reply_likes')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(like_2.id, response.data[0]['id'])
        self.assertEqual(like_2.user_id, response.data[0]['user']['id'])
        self.assertEqual(like_2.user.username, response.data[0]['user']['username'])
        self.assertEqual(like_1.id, response.data[1]['id'])
        self.assertEqual(like_1.user_id, response.data[1]['user']['id'])
        self.assertEqual(like_1.user.username, response.data[1]['user']['username'])

    def test_should_delete_reply_like(self):
        self.client.force_authenticate(user=self.test_user)
        entry = ReplyLike.objects.create(reply=self.test_replies[0], user=self.test_user)

        response = self.client.delete(f'/api/reply_likes/{entry.id}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Reply.objects.filter(id=entry.id).exists())
        self.assertEqual(Reply.objects.get(id=self.test_replies[0].id).like_count, 0)
