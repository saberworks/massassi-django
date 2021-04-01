import os

from django.db import models
from django.utils import timezone
from imagekit.models import ImageSpecField
from pilkit.processors import Thumbnail

from massassi.models import MassassiBaseModel, MassassiModelWithFile

from .util import get_screenshot_1_upload_path, get_screenshot_2_upload_path

class LevelCategory(MassassiBaseModel):
    path = models.CharField(max_length=16, null=False)
    name = models.CharField(max_length=64, null=False)
    description = models.TextField(null=True, blank=True)
    enable_3dpreview = models.BooleanField(null=False, default=False)
    game = models.CharField(max_length=16, null=True)

    def __str__(self):
        return "{} (/{}/ id:{})".format(self.name, self.path, self.id)

    class Meta:
        verbose_name_plural = 'Level Categories'


class Level(MassassiBaseModel, MassassiModelWithFile):
    category = models.ForeignKey('LevelCategory', on_delete=models.CASCADE)
    name = models.CharField(max_length=128, blank=False)
    description = models.TextField(blank=False)
    author = models.CharField(max_length=128, blank=False)
    email = models.EmailField(blank=False)
    dl_count = models.PositiveIntegerField(null=False, blank=False, default=0)
    comment_count = models.PositiveIntegerField(null=False, blank=False, default=0)
    rate_count = models.PositiveIntegerField(null=False, blank=False, default=0)
    rating = models.PositiveIntegerField(null=True, blank=True, default=None)

    # 2 possible screenshots
    screenshot_1 = models.ImageField(upload_to=get_screenshot_1_upload_path, null=True)
    thumbnail_1 = ImageSpecField(source='screenshot_1',
                                 processors=[Thumbnail(400, 200)],
                                 format='JPEG',
                                 options={'quality': 85})

    screenshot_2 = models.ImageField(upload_to=get_screenshot_2_upload_path, null=True)
    thumbnail_2 = ImageSpecField(source='screenshot_2',
                                 processors=[Thumbnail(400, 200)],
                                 format='JPEG',
                                 options={'quality': 85})

    def get_file_upload_to(self, filename):
        return os.path.join(
            "levels/files/{}/{}".format(self.category.path, filename)
        )

    def save(self, *args, **kwargs):
        if self.pk is None:
            saved_screenshot_1 = self.screenshot_1
            saved_screenshot_2 = self.screenshot_2
            self.screenshot_1 = None
            self.screenshot_2 = None
            super().save(*args, **kwargs)
            self.screenshot_1 = saved_screenshot_1
            self.screenshot_2 = saved_screenshot_2

        super().save(*args, **kwargs)

    def __str__(self):
        return "{} ({})".format(self.name, self.id)


class LevelComment(MassassiBaseModel):
    level = models.ForeignKey('Level', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    comment = models.TextField(blank=False, null=False)
    ip = models.GenericIPAddressField(null=False, blank=False, default='0.0.0.0')
    date_created = models.DateTimeField(null=False, blank=False, default=timezone.now)


class LevelRating(MassassiBaseModel):
    level = models.ForeignKey('Level', on_delete=models.CASCADE)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(null=False, blank=False, default='0.0.0.0')
    rating = models.PositiveSmallIntegerField(null=False, blank=False)
    date_created = models.DateTimeField(null=False, blank=False, default=timezone.now)
