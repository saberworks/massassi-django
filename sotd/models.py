from django.db import models
from imagekit.models import ImageSpecField
from pilkit.processors import Thumbnail

from massassi.models import MassassiBaseModel


class SotD(MassassiBaseModel):
    sotd_date = models.DateField(null=False)
    admin_id = models.IntegerField(null=False)
    title = models.CharField(max_length=64, null=False)
    author = models.CharField(max_length=64, null=False)
    author_email = models.EmailField(null=True)
    url = models.URLField(null=True)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to='sotd', null=False)
    thumbnail = ImageSpecField(source='image',
                               processors=[Thumbnail(400, 200)],
                               format='JPEG',
                               options={'quality': 85})

    def __str__(self):
        return "{} ({})".format(self.sotd_date, self.id)

    class Meta:
        verbose_name = 'Screenshot of the Day'
        verbose_name_plural = 'Screenshots of the Day'
        db_table = 'sotd'
