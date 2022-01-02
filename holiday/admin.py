from django.contrib import admin
from django.utils.html import format_html

from massassi.admin import MassassiModelAdmin
from .models import HolidayLogo

class HolidayLogoAdmin(MassassiModelAdmin):
    list_display = ('image_tag', 'year', 'author', 'is_enabled', 'is_in_rotation')
    list_per_page = 40
    search_fields = ('year', 'author')
    list_filter = ('is_enabled', 'is_in_rotation',)
    fields = ('logo', 'year', 'author', 'is_enabled', 'is_in_rotation')

    def get_ordering(self, request):
        return ['-year', 'author']

    def image_tag(self,obj):
        return format_html('<img src="{0}" style="width: 300px;" />'.format(obj.logo.url))

admin.site.register(HolidayLogo, HolidayLogoAdmin)
