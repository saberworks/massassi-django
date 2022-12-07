import os
from random import randint

from django.db import models

from massassi.models import MassassiBaseModel

def get_holiday_upload_path(instance, filename):
    return os.path.join(
        'holiday_logos/{}/{}'.format(instance.year, filename)
    )

class HolidayLogoManager(models.Manager):
    def random(self):
        return self.filter(is_in_rotation=True).order_by('?').first()

class HolidayLogo(MassassiBaseModel):
    author = models.CharField(max_length=32, null=False, blank=False)
    year = models.PositiveSmallIntegerField(null=False, blank=False)
    logo = models.ImageField(upload_to=get_holiday_upload_path, null=False, blank=False)
    is_enabled = models.BooleanField(default=True)
    is_in_rotation = models.BooleanField(default=True)

    objects = HolidayLogoManager()

    def __str__(self):
        return "{}-{} ({})".format(self.year, self.author, self.pk)

    def admin_image(self):
        return '<img src="%s"/>' % self.logo

    admin_image.allow_tags = True

    class Meta:
        verbose_name_plural = 'Holiday Logos'
        db_table = 'holiday_logos'
        indexes = [
            models.Index(fields=['is_in_rotation']),
        ]
