import hashlib
import logging
import os

from colorfield.fields import ColorField
from django.conf import settings
from django.db import models
from django.utils import timezone
from django_s3_storage.storage import S3Storage
from imagekit.models import ImageSpecField
from pilkit.processors import Thumbnail
from pprint import pprint

s3bucket = settings.AWS_BUCKET_SABERWORKS
s3storage = S3Storage(aws_s3_bucket_name=s3bucket)


logger = logging.getLogger(__name__)

#
# This is a re-implementation of the MassassiModelWithImage and
# MassassiModelWithFile abstract classes because saberworks.net will store
# files in s3 (rather than locally).  I couldn't find a way to inherit from
# the original abstract class and override just the storage without having
# to redefine every field from scratch anyway.
#

# If table will have a single file, always store file location, file size,
# file checksum.
#
# Every model that inherits from this _must_ provide a unique
# get_file_upload_to method.  WARNING: Do not make the file name generation
# require the model's ID, because the ID won't exist yet on initial save of the
# model.
def get_file_upload_to(instance, filename):
    return instance.get_file_upload_to(filename)

class SaberworksModelWithFile(models.Model):
    file = models.FileField(upload_to=get_file_upload_to, null=True, storage=s3storage)
    file_size = models.PositiveIntegerField(null=True, blank=True)
    file_hash = models.CharField(max_length=40, blank=True, editable=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


        if(self.file):
            conn = s3storage.s3_connection

            details = conn.head_object(
                Bucket=s3bucket,
                Key=str(self.file.name),
            )

            pprint(details)

            self.file_hash = details.get("ETag").replace('"', '')
            self.file_size = details.get("ContentLength")
            self.name = os.path.basename(self.file.name)

            super().save(update_fields=['file_hash', 'file_size', 'name'])

    class Meta:
        abstract = True

# Every model that inherits from this _must_ provide a unique
# get_image_upload_to method.  WARNING: Do not make the image name
# require the model's ID, because the ID won't exist on initial save of
# model.
def get_image_upload_to(instance, filename):
    return instance.get_image_upload_to(filename)

class SaberworksModelWithImage(models.Model):
    image = models.ImageField(upload_to=get_image_upload_to, null=True, blank=True, storage=s3storage)
    thumbnail = ImageSpecField(
        source='image',
        processors=[Thumbnail(400, 300)],
        format='JPEG',
        options={'quality': 85},
    )

    class Meta:
        abstract = True

class SaberworksModelWithColor(models.Model):
    color = ColorField(null=True, blank=True, default=None)

    class Meta:
        abstract = True
