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
        count = self.count()
        random_index = randint(0, count - 1)
        return self.all()[random_index]

class HolidayLogo(MassassiBaseModel):
    author = models.CharField(max_length=32, null=False, blank=False)
    year = models.PositiveSmallIntegerField(null=False, blank=False)
    logo = models.ImageField(upload_to=get_holiday_upload_path, null=False, blank=False)
    is_enabled = models.BooleanField(default=True)
    is_in_rotation = models.BooleanField(default=True)

    objects = HolidayLogoManager()

    class Meta:
        verbose_name_plural = 'Holiday Logos'
        db_table = 'holiday_logos'
