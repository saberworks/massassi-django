from django.contrib import admin
from django.utils.html import format_html

from massassi.admin import MassassiModelAdmin
from .models import TagType, Tag, Game, Project, Post, File

class TagTypeAdmin(MassassiModelAdmin):
    list_display = ('slug', 'created_by')
    list_filter = (
        ('created_by', admin.RelatedOnlyFieldListFilter),
    )
    ordering = ('slug',)
    readonly_fields = ('created_by',)
    fields = ('slug',)

class TagAdmin(MassassiModelAdmin):
    list_display = ('type', 'slug')
    list_filter = (
        ('created_by', admin.RelatedOnlyFieldListFilter),
    )
    ordering = ('type', 'slug',)
    readonly_fields = ('created_by',)
    fields = ('type', 'slug',)

class GameAdmin(MassassiModelAdmin):
    list_display = ('name', 'slug', 'created_by')
    list_filter = (
        ('created_by', admin.RelatedOnlyFieldListFilter),
    )
    ordering = ('name',)
    readonly_fields = ('created_by',)
    fields = ('name', 'slug', 'description', 'image',)

class ProjectAdmin(MassassiModelAdmin):
    list_display = ('name', 'slug', 'user', 'accent_color_tag')
    ordering = ('name',)
    readonly_fields = ('created_by', 'user', 'slug',)
    fields = ('name', 'games', 'description', 'tags', 'image', 'accent_color', 'slug')

    def accent_color_tag(self, obj):
        return format_html('<span style="color: #{0}">{0}</span>'.format(obj.accent_color))

class PostAdmin(MassassiModelAdmin):
    list_display = ('title', 'slug', 'project', 'user',)
    ordering = ('title',)
    readonly_fields = ('created_by', 'user',)
    fields = ('title', 'project', 'text', 'image', 'user')

class FileAdmin(MassassiModelAdmin):
    list_display = ('project', 'name', 'version', 'user', 'name', 'version')
    ordering = ('-created_at',)
    readonly_fields = ('file_hash', 'file_size', 'created_by',)
    fields = ('project', 'name', 'description', 'image', 'version', 'file')


admin.site.register(TagType, TagTypeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(File, FileAdmin)
