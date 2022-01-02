from django.contrib import admin
from django.utils.html import format_html

from massassi.admin import MassassiModelAdmin
from .models import SotD


class SotdAdmin(MassassiModelAdmin):
    list_display = ('image_tag', 'sotd_date', 'title', 'author', 'author_email')
    list_per_page = 40
    fields = ('sotd_date', 'author', 'author_email', 'url', 'title', 'description', 'image')
    
    # This is here because the sotd table has a `user_id` column; it's an
    # artifact of the old system maybe?  But it records the same info as
    # `created_by`.  Just keeping it around for now but will eventually remove
    # the entire column.
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def image_tag(self,obj):
        return format_html('<img src="{0}" style="width: 300px;" />'.format(obj.thumbnail.url))


admin.site.register(SotD, SotdAdmin)
