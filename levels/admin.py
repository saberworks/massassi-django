from django.contrib import admin

from massassi.admin import MassassiModelAdmin
from .models import Level, LevelCategory, LevelComment

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

class LevelCommentAdmin(MassassiModelAdmin):
    list_display = ('id', 'level', 'user', 'comment', 'ip', 'date_created')
    # list_display_links = ('id', 'level', 'user')
    search_fields = ('id', 'level__name', 'user__username', 'comment', 'ip', 'date_created')
    readonly_fields = ('id', 'level', 'user', 'comment', 'ip', 'date_created')
    fields = ('id', 'level', 'user', 'comment', 'ip', 'date_created')

admin.site.register(LevelComment, LevelCommentAdmin)
