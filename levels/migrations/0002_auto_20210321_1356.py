# Generated by Django 3.1.7 on 2021-03-21 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('levels', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='levelcategory',
            options={'verbose_name_plural': 'Level Categories'},
        ),
        migrations.AddField(
            model_name='levelcategory',
            name='game',
            field=models.CharField(max_length=16, null=True),
        ),
    ]
