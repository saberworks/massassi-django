from django.contrib import admin
from django.utils.html import format_html

from massassi.admin import MassassiModelAdmin
from .models import LotwHistory

class LotwHistoryAdmin(MassassiModelAdmin):
    list_display = ('image_tag', 'lotw_time', 'level_name')
    list_per_page = 40
    fields = ('lotw_time','level')
    autocomplete_fields = ['level',]
    
    # results in an extra query per row... urgh
    def image_tag(self,obj):
        if(obj.level.screenshot_1):
            return format_html('<img src="{0}" style="width: 300px;" />'.format(obj.level.screenshot_1.url))
        else:
            return "No Screenshot"

    # results in ANOTHER extra query per row... urgh
    def level_name(self, obj):
        return obj.level.name

admin.site.register(LotwHistory, LotwHistoryAdmin)
