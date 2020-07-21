import io

from model_bakery import baker
from munch import Munch
from rest_framework import status
from rest_framework.test import APITestCase

from PIL import Image

from stories.models import Story, StoryViewCheck
from users.models import User


class StoryTestCase(APITestCase):
    @staticmethod
    def temporary_image():
        file = io.BytesIO()
        image = Image.new('RGB', (1, 1))
        image.save(file, 'jpeg')
        file.name = 'test.jpg'
        file.seek(0)
        return file

    def setUp(self):
        self.test_users = baker.make('users.User', _quantity=2)
        self.test_follows = baker.make('follows.Follow', following=self.test_users[0], _quantity=2)
        self.image_name = 'test.jpg'
        self.data = {'story_text': 'for test', 'story_image': self.temporary_image()}

    def test_should_create_story(self):
        self.client.force_authenticate(user=self.test_users[0])
        response = self.client.post(f'/api/users/{self.test_users[0].id}/stories',
                                    data=self.data, format='multipart')

        story_response = Munch(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response)
        self.assertTrue(story_response.id)
        self.assertEqual(story_response['user']['id'], self.test_users[0].id)
        self.assertEqual(story_response.story_text, self.data['story_text'])
        self.assertEqual(story_response.image_name, self.image_name)
        self.assertTrue('.jpg' in story_response.story_image)

    def test_should_list_new_stories_by_owner(self):
        self.client.force_authenticate(user=self.test_users[0])
        stories = baker.make('stories.Story',
                             user=self.test_users[0],
                             story_image=self.temporary_image().name,
                             _quantity=2)
        response = self.client.get(f'/api/users/{self.test_users[0].id}/stories')

        self.assertEqual(response.status_code, status.HTTP_200_OK, response)
        for entry, response_entry in zip(stories, response.data):
            self.assertEqual(entry.id, response_entry['id'])
            self.assertEqual(entry.story_text, response_entry['story_text'])
            self.assertTrue('.jpg' in response_entry['story_image'])
            self.assertEqual(entry.user.id, response_entry['user']['id'])
            self.assertEqual(entry.user.username, response_entry['user']['username'])

    def test_should_list_only_created_less_then_24hours(self):
        self.client.force_authenticate(user=self.test_users[0])
        valid_story = baker.make('stories.Story',
                                 user=self.test_users[0],
                                 story_image=self.temporary_image().name)
        # invalid_story : 하루 이상 지난 스토리
        invalid_story = baker.make('stories.Story',
                                   user=self.test_users[0],
                                   story_image=self.temporary_image().name,
                                   time_stamp='2020-07-19T11:19:15.369605Z')
        response = self.client.get(f'/api/users/{self.test_users[0].id}/stories')

        self.assertEqual(response.status_code, status.HTTP_200_OK, response)
        self.assertEqual(response.data[0]['id'], valid_story.id)
        self.assertEqual(response.data[0]['story_text'], valid_story.story_text)
        self.assertTrue('.jpg' in response.data[0]['story_image'])
        self.assertEqual(response.data[0]['user']['id'], valid_story.user.id)

    def test_should_list_only_followers_can_view(self):
        valid_story = baker.make('stories.Story',
                                 user=self.test_users[0],
                                 story_image=self.temporary_image().name)
        # follower : story owner를 following 하고 있는 유저
        follower = User.objects.get(id=self.test_follows[0].follower.id)

        self.client.force_authenticate(user=follower)
        response = self.client.get(f'/api/users/{self.test_users[0].id}/stories')

        self.assertEqual(response.status_code, status.HTTP_200_OK, response)
        self.assertEqual(User.objects.filter(followings__follower=follower).count(), 1)
        self.assertEqual(response.data[0]['id'], valid_story.id)
        self.assertEqual(response.data[0]['story_text'], valid_story.story_text)
        self.assertTrue('.jpg' in response.data[0]['story_image'])
        self.assertEqual(response.data[0]['user']['id'], valid_story.user.id)

    def test_should_update_story(self):
        data = {'story_text': 'changed', 'story_image': self.temporary_image()}
        self.client.force_authenticate(user=self.test_users[0])
        entry = Story.objects.create(user=self.test_users[0], story_image=self.temporary_image().name)
        prev_text = entry.story_text
        prev_image = entry.story_image

        response = self.client.put(f'/api/users/{self.test_users[0].id}/stories/{entry.id}',
                                   data=data, format='multipart')

        response_entry = Munch(response.data)
        self.assertNotEqual(prev_text, response_entry.story_text)
        self.assertEqual(data['story_text'], response_entry.story_text)
        self.assertNotEqual(prev_image, response_entry.story_image)
        self.assertEqual(data['story_image'].name, response_entry.image_name)
        self.assertEqual(entry.id, response_entry.id)
        self.assertEqual(entry.user_id, response_entry['user']['id'])

    def test_should_delete_story(self):
        self.client.force_authenticate(user=self.test_users[0])
        entry = Story.objects.create(user=self.test_users[0], story_image=self.temporary_image().name)

        response = self.client.delete(f'/api/stories/{entry.id}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, response)
        self.assertFalse(Story.objects.filter(id=entry.id).exists())

    def test_should_retrieve_story(self):
        valid_story = baker.make('stories.Story',
                                 user=self.test_users[0],
                                 story_image=self.temporary_image().name)
        follower = User.objects.get(id=self.test_follows[0].follower.id)
        self.client.force_authenticate(user=follower)

        response = self.client.get(f'/api/users/{self.test_users[0].id}/stories/{valid_story.id}')

        self.assertEqual(StoryViewCheck.objects.filter(user=follower).count(), 1)
        self.assertEqual(StoryViewCheck.objects.get(user=follower).story.id, valid_story.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK, response)
        self.assertEqual(response.data['id'], valid_story.id)
        self.assertEqual(response.data['story_text'], valid_story.story_text)
        self.assertTrue('.jpg' in response.data['story_image'])
        self.assertEqual(response.data['user']['id'], valid_story.user.id)