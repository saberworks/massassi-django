# Generated by Django 3.2.10 on 2022-01-03 06:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SotD',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_modified_at', models.DateTimeField(auto_now=True)),
                ('sotd_date', models.DateField(unique=True)),
                ('title', models.CharField(max_length=64)),
                ('author', models.CharField(max_length=64)),
                ('author_email', models.EmailField(max_length=254, null=True)),
                ('url', models.URLField(null=True)),
                ('description', models.TextField(null=True)),
                ('image', models.ImageField(upload_to='sotd')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('last_modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Screenshot of the Day',
                'verbose_name_plural': 'Screenshots of the Day',
                'db_table': 'sotd',
            },
        ),
    ]
