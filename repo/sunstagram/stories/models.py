import datetime

from django.db import models
from django.utils import timezone
from uuid_upload_path import upload_to


class Story(models.Model):
    user = models.ForeignKey('users.User', related_name='story_owners', on_delete=models.CASCADE)
    story_text = models.CharField(max_length=255, default='')
    time_stamp = models.DateTimeField(default=timezone.now)
    story_image = models.ImageField(upload_to=upload_to)  # generate uuid path
    image_name = models.CharField(max_length=50)

    def was_created_in_24hours(self):
        now = timezone.now()
        return (now - datetime.timedelta(days=1)) <= self.time_stamp <= now

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.image_name = self.story_image.name
        super().save(force_insert, force_update, using, update_fields)


class StoryViewCheck(models.Model):
    """
    Only story-owner's followings can view story
    """
    story = models.ForeignKey('stories.Story', related_name='stories', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', related_name='story_viewers', on_delete=models.CASCADE)
