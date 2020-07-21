from model_bakery import baker
from munch import Munch
from rest_framework import status
from rest_framework.test import APITestCase

from comments.models import Comment
from replies.models import Reply


class CommentTestCase(APITestCase):
    def setUp(self):
        self.test_user = baker.make('users.User', username='test')
        self.test_post = baker.make('feeds.Post', user=self.test_user, post_text='hi')
        self.test_comments = baker.make('comments.Comment',
                                        post=self.test_post,
                                        user=self.test_user,
                                        _quantity=2)
        self.comment = self.test_comments[0]

    def test_should_create_comment(self):
        self.client.force_authenticate(user=self.test_user)
        data = {'comment_text': 'for test'}

        response = self.client.post(f'/api/posts/{self.test_post.id}/comments', data=data)

        comment_response = Munch(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(comment_response.id)
        self.assertEqual(comment_response.comment_text, data['comment_text'])
        self.assertEqual(comment_response.reply_count, 0)
        self.assertTrue(comment_response.user['id'])
        self.assertEqual(comment_response.user['username'], self.test_user.username)
        self.assertEqual(comment_response.user['profile_image'], 'http://testserver/profile_images/default.jpg')

    def test_should_list_comments(self):
        response = self.client.get(f'/api/posts/{self.test_post.id}/comments')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(Comment.objects.all().count(), 2)
        for comment, comment_response in zip(self.test_comments[::-1], response.data):
            self.assertEqual(comment.id, comment_response['id'])
            self.assertEqual(comment.comment_text, comment_response['comment_text'])
            self.assertEqual(comment.user.username, comment_response['user']['username'])
            self.assertEqual(comment.user.userprofile.profile_image, 'profile_images/default.jpg')

    def test_should_update_comment(self):
        self.client.force_authenticate(user=self.test_user)
        baker.make('replies.Reply', user=self.test_user, comment=self.comment, _quantity=2)
        data = {'comment_text': 'changed'}

        response = self.client.put(f'/api/posts/{self.test_post.id}/comments/{self.comment.id}', data=data)

        comment_response = Munch(response.data)
        self.assertEqual(self.comment.id, comment_response.id)
        self.assertEqual(comment_response.reply_count,
                         Reply.objects.filter(comment=self.comment, user=self.test_user).count())
        self.assertNotEqual(self.comment.comment_text, comment_response.comment_text)

    def test_should_delete_comment(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.delete(f'/api/comments/{self.comment.id}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())


class ReplyTestCase(APITestCase):
    def setUp(self):
        self.test_user = baker.make('users.User', username='test')
        self.test_post = baker.make('feeds.Post', user=self.test_user)
        self.test_comments = baker.make('comments.Comment',
                                        post=self.test_post,
                                        user=self.test_user,
                                        _quantity=2)
        self.comment = self.test_comments[0]
        self.test_replies = baker.make('replies.Reply',
                                       user=self.test_user,
                                       comment=self.comment,
                                       _quantity=2)

    def test_should_create_reply(self):
        self.client.force_authenticate(user=self.test_user)
        data = {'reply_text': 'for test'}
        response = self.client.post(f'/api/comments/{self.comment.id}/replies', data=data)

        reply_response = Munch(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(reply_response.id)
        self.assertEqual(reply_response.reply_text, data['reply_text'])
        self.assertTrue(reply_response.user['id'])
        self.assertEqual(reply_response.user['username'], self.test_user.username)
        self.assertEqual(reply_response.user['profile_image'], 'http://testserver/profile_images/default.jpg')

    def test_should_list_replies(self):
        response = self.client.get(f'/api/comments/{self.comment.id}/replies')

        self.assertEqual(Reply.objects.all().count(), 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for reply, reply_response in zip(self.test_replies, response.data):
            self.assertEqual(reply.id, reply_response['id'])
            self.assertEqual(reply.reply_text, reply_response['reply_text'])
            self.assertEqual(reply.user.username, self.test_user.username)
            self.assertEqual(reply.user.userprofile.profile_image, 'profile_images/default.jpg')

    def test_should_update_reply(self):
        self.client.force_authenticate(user=self.test_user)
        data = {'reply_text': 'changed'}
        entry = self.test_replies[0]
        response = self.client.put(f'/api/comments/{self.comment.id}/replies/{entry.id}', data=data)

        reply_response = Munch(response.data)
        self.assertEqual(entry.id, reply_response.id)
        self.assertNotEqual(entry.reply_text, reply_response.reply_text)

    def test_should_delete_reply(self):
        self.client.force_authenticate(user=self.test_user)
        entry = self.test_replies[0]
        response = self.client.delete(f'/api/replies/{entry.id}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Reply.objects.filter(id=entry.id).exists())
