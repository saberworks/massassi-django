from django.contrib import admin

from .models import LevelCategory, Level


class LevelCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'path', 'game', 'enable_3dpreview')


admin.site.register(LevelCategory, LevelCategoryAdmin)

class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'author')


admin.site.register(Level, LevelAdmin)
