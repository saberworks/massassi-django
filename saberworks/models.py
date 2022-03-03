import logging
import os

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields import SlugField
from django.utils.text import slugify

from massassi.models import MassassiBaseModel, MassassiModelWithFile, MassassiModelWithImage

logger = logging.getLogger(__name__)


# TagTypes
class TagType(MassassiBaseModel):
    slug = SlugField(max_length=40, null=False, blank=False)

    def __str__(self):
        return self.slug

# Tags
class TagManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('type')

class Tag(MassassiBaseModel):
    type = models.ForeignKey('saberworks.TagType', null=False, blank=False, on_delete=models.RESTRICT)
    slug = SlugField(max_length=40, null=False, blank=False, unique=True)

    objects = TagManager

    def __str__(self):
        return self.type.slug + ':' + self.slug

# Games
# Adding games is an admin task so no need to autogenerate slugs.
class Game(MassassiBaseModel, MassassiModelWithImage):
    name = models.CharField(max_length=64, null=False, blank=False)
    slug = models.SlugField(max_length=40, null=False, blank=False, unique=True)
    description = models.TextField(null=True, blank=True)

    def get_image_upload_to(self, filename):
        return 'saberworks/game/{}'.format(filename)

    def __str__(self):
        return self.name

# Projects
class Project(MassassiBaseModel, MassassiModelWithImage):
    user = models.ForeignKey('users.User', null=False, blank=False, on_delete=models.RESTRICT)
    games = models.ManyToManyField('saberworks.Game', blank=True)
    tags = models.ManyToManyField('saberworks.Tag', blank=True)
    name = models.CharField(max_length=256, null=False, blank=False)
    slug = models.SlugField(max_length=40, null=False, blank=False, editable=False, unique=True)
    description = models.TextField(blank=True)
    accent_color = models.CharField(max_length=6, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.slug = slugify(str(self.pk) + '-' + self.name, allow_unicode=False)

        super().save()

    def get_image_upload_to(self, filename):
        return 'saberworks/project/{}/{}'.format(self.slug, filename)

    def __str__(self):
        return 'id=' + str(self.pk) + ' name=' + self.name

class Screenshot(MassassiBaseModel, MassassiModelWithImage):
    user = models.ForeignKey('users.User', null=False, blank=False, on_delete=models.RESTRICT)
    project = models.ForeignKey('saberworks.Project', null=False, blank=False, on_delete=models.RESTRICT)

    def get_image_upload_to(self, filename):
        return 'saberworks/project/{}/images/{}'.format(self.project.slug, filename)

# Posts (can contain text, image, or both)
class Post(MassassiBaseModel, MassassiModelWithImage):
    user = models.ForeignKey('users.User', null=False, blank=False, on_delete=models.RESTRICT)
    project = models.ForeignKey('saberworks.Project', null=False, blank=False, on_delete=models.RESTRICT)
    title = models.CharField(max_length=256, null=False, blank=False)
    slug = models.SlugField(max_length=40, null=False, blank=False, editable=False, unique=True)
    text = models.TextField(null=False, blank=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.slug = slugify(str(self.pk) + '-' + self.title, allow_unicode=False)

        super().save()

    def get_image_upload_to(self, filename):
        return 'saberworks/project/{}/{}'.format(self.project.slug, filename)

    def __str__(self):
        return 'id=' + str(self.pk) + ' title=' + self.title

    class Meta:
        ordering = ['-created_at']

# Files
class File(MassassiBaseModel, MassassiModelWithFile, MassassiModelWithImage):
    user = models.ForeignKey('users.User', null=False, blank=False, on_delete=models.RESTRICT)
    project = models.ForeignKey('saberworks.Project', null=False, blank=False, on_delete=models.RESTRICT)
    name = models.CharField(max_length=256, null=False, blank=False)
    version = models.CharField(max_length=16, null=False, blank=False)
    description = models.TextField(blank=False)

    def get_file_upload_to(self, filename):
        # saberworks/{project_slug}/{version}/{name}.ext
        project_slug = self.project.slug
        version = self.version

        return os.path.join(
            "saberworks/project/{}/{}/{}".format(project_slug, version, filename)
        )

    def get_image_upload_to(self, filename):
        # saberworks/{project_slug}/{version}/{filename}
        project_slug = self.project.slug
        version = self.version

        return os.path.join(
            "saberworks/project/{}/{}/{}".format(project_slug, version, filename)
        )

    def __str__(self):
        return 'id=' + str(self.pk) + ' name=' + self.name + ' version=' + self.version
