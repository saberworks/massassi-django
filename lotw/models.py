from django.db import models

from massassi.models import MassassiBaseModel


class LotwHistory(MassassiBaseModel):
    lotw_time = models.DateTimeField(null=False)
    level = models.ForeignKey('levels.Level', related_name='+', on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        verbose_name = 'Level of the Week'
        verbose_name_plural = 'Levels of the Week'
        db_table = 'lotw_history'

class LotwVote(MassassiBaseModel):
    user = models.ForeignKey('users.User', related_name='+', on_delete=models.CASCADE, null=False, blank=False)
    level = models.ForeignKey('levels.Level', related_name='+', on_delete=models.CASCADE, null=False, blank=False)
    voted_at = models.DateTimeField(null=False)
    ip = models.GenericIPAddressField(null=False, blank=False, default='0.0.0.0')

    class Meta:
        verbose_name = 'Level of the Week Vote'
        verbose_name_plural = 'Level of the Week Votes'
        db_table = 'lotw_votes'
