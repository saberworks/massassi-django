from django.contrib import admin

from .models import LevelCategory, Level


class LevelCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'path', 'game', 'enable_3dpreview')


admin.site.register(LevelCategory, LevelCategoryAdmin)

class LevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'author')
    search_fields = ('id', 'name', 'author')


admin.site.register(Level, LevelAdmin)
