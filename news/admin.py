from django.contrib import admin
from django.contrib.auth import get_user_model

from massassi.admin import MassassiModelAdmin
from .models import News


class NewsAdmin(MassassiModelAdmin):
    list_display = ('headline', 'user', 'date_posted',)
    list_filter = (
        ('user', admin.RelatedOnlyFieldListFilter),
    )
    ordering = ('-date_posted',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields = ('date_posted', 'headline', 'story', 'user') + self.get_default_fields()
        self.fields = ('date_posted', 'headline', 'story', 'user') + self.fields

    # When creating a form, default the user field to currently loggeed-in user
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['user'].initial = request.user
        return form

    # Only allow staff members as the "user" (owner/creator) of a news item
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['queryset'] = get_user_model().objects.filter(is_staff=True).order_by('username')

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(News, NewsAdmin)
