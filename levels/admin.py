from django.contrib import admin

from massassi.admin import MassassiModelAdmin
from .models import LevelCategory, Level

class LevelCategoryAdmin(MassassiModelAdmin):
    list_display = ('id', 'name', 'path', 'game', 'enable_3dpreview')
    fields = ('name', 'path', 'game', 'enable_3dpreview')


admin.site.register(LevelCategory, LevelCategoryAdmin)

class LevelAdmin(MassassiModelAdmin):
    list_display = ('id', 'name', 'category', 'author', 'last_modified_at')
    search_fields = ('id', 'name', 'author')
    readonly_fields = ('file_hash', 'file_size', 'dl_count', 'rate_count', 'rating', 'comment_count')
    fields = (
        'category', 'name', 'description', 'author', 'email', 'file',
        'file_hash', 'file_size', 'screenshot_1', 'screenshot_2',
        'dl_count', 'comment_count', 'rate_count', 'rating'
    )

admin.site.register(Level, LevelAdmin)
