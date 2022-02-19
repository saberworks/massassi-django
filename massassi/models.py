import hashlib

from django.db import models
from django.utils import timezone
from imagekit.models import ImageSpecField
from pilkit.processors import Thumbnail


#
# All models should inherit from this, it adds fields for tracking
# creation/modification time and creation/modification user.
#
class MassassiBaseModel(models.Model):
    created_at = models.DateTimeField(null=False, blank=False, default=timezone.now)
    created_by = models.ForeignKey('users.User', related_name='+', on_delete=models.CASCADE, null=True, blank=True)
    last_modified_at = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey('users.User', related_name='+', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        abstract = True

# If table will have a single file, always store file location, file size,
# file checksum.
# Problem with this approach is that I need to be able to pass a function to
# the models.FileField so that it can dynamically get the location for the
# uploaded file.  Maybe every child has to manually set it? :(  Example:
#
# FakeModel._meta.get_field('email').upload_to = some_func

def get_file_upload_to(instance, filename):
    return instance.get_file_upload_to(filename)

class MassassiModelWithFile(models.Model):
    file = models.FileField(upload_to=get_file_upload_to, null=True)
    file_size = models.PositiveIntegerField(null=True, blank=True)
    file_hash = models.CharField(max_length=40, blank=True, editable=False)

    def save(self, *args, **kwargs):
        self.file_size = self.file.file.size

        super().save(*args, **kwargs)

        with open(self.file.path, "rb") as f:
            file_hash = hashlib.sha1()
            while chunk := f.read(8192):
                file_hash.update(chunk)

        self.file_hash = file_hash.hexdigest()

        super().save()

    class Meta:
        abstract = True

# Every model that inherits from this _must_ provide a unique
# get_image_upload_to method.  WARNING: Do not make the image name
# require the image ID, because the ID won't exist on initial save of
# each model.
def get_image_upload_to(instance, filename):
    return instance.get_image_upload_to(filename)

class MassassiModelWithImage(models.Model):
    image = models.ImageField(upload_to=get_image_upload_to, null=True, blank=True)
    thumbnail = ImageSpecField(
        source='image',
        processors=[Thumbnail(400, 300)],
        format='JPEG',
        options={'quality': 85},
    )

    class Meta:
        abstract = True
