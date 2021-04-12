from django.db import models

from massassi.models import MassassiBaseModel


class HolidayLogo(MassassiBaseModel):
    author = models.CharField(max_length=32, null=False, blank=False)
    year = models.PositiveSmallIntegerField(null=False, blank=False)
    logo = models.ImageField(upload_to='holiday_logos', null=False, blank=False)
    is_enabled = models.BooleanField(default=True)
    is_in_rotation = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Holiday Logos'
        db_table = 'holiday_logos'
