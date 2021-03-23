# Generated by Django 3.1.7 on 2021-03-23 07:47

from django.db import migrations, models
import levels.models


class Migration(migrations.Migration):

    dependencies = [
        ('levels', '0004_remove_level_filename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='level',
            name='file',
            field=models.FileField(null=True, upload_to=levels.models.get_upload_path),
        ),
        migrations.AlterField(
            model_name='level',
            name='filesize',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='level',
            name='screenshot_1',
            field=models.ImageField(null=True, upload_to=levels.models.get_screenshot_1_upload_path),
        ),
        migrations.AlterField(
            model_name='level',
            name='screenshot_2',
            field=models.ImageField(null=True, upload_to=levels.models.get_screenshot_2_upload_path),
        ),
        migrations.AlterField(
            model_name='levelcategory',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
