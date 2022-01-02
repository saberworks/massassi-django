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
    readonly_fields = ('user',)
    fields = ('date_posted', 'headline', 'story', 'user')

    # This is here because the news table has a `user_id` column; it's an
    # artifact of the old system.  It records the same info as `created_by`.
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(News, NewsAdmin)
