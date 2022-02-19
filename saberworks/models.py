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

# Tags (need tags_projects join table, is it automatic?)
class Tag(MassassiBaseModel):
    type = models.ForeignKey('saberworks.TagType', null=False, blank=False, on_delete=models.RESTRICT)
    slug = SlugField(max_length=40, null=False, blank=False)

    def __str__(self):
        return self.type.slug + ':' + self.slug

# Games
class Game(MassassiBaseModel, MassassiModelWithImage):
    name = models.CharField(max_length=64, null=False, blank=False)
    slug = models.SlugField(max_length=40, null=False, blank=False, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_image_upload_to(self, filename):
        return 'saberworks/game/{}'.format(filename)

# Projects
class Project(MassassiBaseModel, MassassiModelWithImage):
    user = models.ForeignKey('users.User', null=False, blank=False, on_delete=models.RESTRICT)
    games = models.ManyToManyField('saberworks.Game')
    tags = models.ManyToManyField('saberworks.Tag')
    name = models.CharField(max_length=256, null=False, blank=False)
    slug = models.SlugField(max_length=40, null=False, blank=False, unique=True)
    description = models.TextField(blank=True)
    accent_color = models.CharField(max_length=6, null=True)

    def get_image_upload_to(self, filename):
        return 'saberworks/project/{}/{}'.format(self.slug, filename)
    
    def __str__(self):
        return self.slug + ': ' + self.name

# Posts (can contain text, image, or both)
class Post(MassassiBaseModel, MassassiModelWithImage):
    user = models.ForeignKey('users.User', null=False, blank=False, on_delete=models.RESTRICT)
    project = models.ForeignKey('saberworks.Project', null=False, blank=False, on_delete=models.RESTRICT)
    title = models.CharField(max_length=256, blank=False)
    slug = models.SlugField(max_length=40, null=False, blank=False, editable=False, unique=True)
    text = models.TextField(blank=True)

    def clean(self):
        cleaned_data = super().clean()

        if not self.text and not self.image:
            raise ValidationError({'text': 'Please add text, an image, or both.'})

        return cleaned_data

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.slug = slugify(str(self.pk) + '-' + self.title, allow_unicode=False)

        super().save()

    def get_image_upload_to(self, filename):
        return 'saberworks/project/{}/{}'.format(self.project.slug, filename)

    def __str__(self):
        return self.slug + ': ' + self.title

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
        return self.project.name + ': ' + self.name + ' v' + self.version
