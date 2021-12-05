from django.contrib import admin

from massassi.admin import MassassiModelAdmin
from .models import SotD


class SotdAdmin(MassassiModelAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields = (
            'sotd_date', 'author', 'author_email',
            'url', 'title', 'description', 'image'
        ) + self.fields

    def save_model(self, request, obj, form, change):
        obj.user = request.user.id
        super(SotdAdmin, self).save_model(request, obj, form, change)


admin.site.register(SotD, SotdAdmin)
