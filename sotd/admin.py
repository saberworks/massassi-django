from django.contrib import admin

from massassi.admin import MassassiModelAdmin
from .models import SotD


class SotdAdmin(MassassiModelAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields = ('author', 'author_email', 'url', 'title', 'description', 'image') + self.fields


admin.site.register(SotD, SotdAdmin)
