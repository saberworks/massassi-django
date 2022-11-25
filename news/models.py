from django.db import models
from django.utils import timezone

from massassi.models import MassassiBaseModel

class News(MassassiBaseModel):
    user = models.ForeignKey('users.User', null=False, blank=False, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128, null=False, blank=False)
    story = models.TextField(null=False, blank=False)
    date_posted = models.DateTimeField(null=False, blank=False, default=timezone.now)

    def get_absolute_url(self):
        month = self.date_posted.month
        year = self.date_posted.year
        return "/news_archive_{}-{}.html#news-item-{}".format(year, month, self.id)

    def __str__(self):
        return "{} ({})".format(self.headline, self.id)

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'
        db_table = 'news'
