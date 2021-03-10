from django.db import models

class LotW(models.Model):
    lotw_date = models.DateField(null=False)
    level_id = models.IntegerField(null=False)
    
    class Meta:
        verbose_name = 'Level of the Week'
        verbose_name_plural = 'Levels of the Week'
