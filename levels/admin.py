from django.contrib import admin

from .models import LevelCategory, Level

class LevelCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'path', 'game', 'enable_3dpreview')


admin.site.register(LevelCategory, LevelCategoryAdmin)

class LevelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'author', 'last_modified_at')
    search_fields = ('id', 'name', 'author')
    readonly_fields = ('last_modified_at','file_hash',)

    # When creating a form, default the user field to currently logged-in user
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        form.base_fields['created_by'].initial = request.user
        form.base_fields['last_modified_by'].initial = request.user

        return form

    # Only show staff users in created_by/last_modified_by.
    # This should be done for every admin file... urgh.
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'created_by' or db_field.name == 'last_modified_by':
            field.queryset = field.queryset.filter(is_staff=True)
        return field

admin.site.register(Level, LevelAdmin)
