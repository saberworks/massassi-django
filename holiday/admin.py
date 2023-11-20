import datetime
import logging

from django.contrib import admin
from django.utils.html import format_html

from massassi.admin import MassassiModelAdmin
from news.models import News
from .models import HolidayLogo

logger = logging.getLogger(__name__)

class HolidayLogoAdmin(MassassiModelAdmin):
    list_display = ('image_tag', 'year', 'author', 'is_enabled', 'is_in_rotation')
    list_per_page = 40
    search_fields = ('year', 'author')
    list_filter = ('is_enabled', 'is_in_rotation',)
    fields = ('logo', 'year', 'author', 'is_enabled', 'is_in_rotation')

    def get_ordering(self, request):
        return ['-id']

    def image_tag(self,obj):
        return format_html('<img src="{0}" style="width: 300px;" />'.format(obj.logo.url))

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # If it's a newly created logo (created via the admin form), post news.
        # If it's an existing logo but the is_in_rotation field changed from False to True, post news.
        should_post_news = change == False or ('is_in_rotation' in form.changed_data and obj.is_in_rotation==True)

        year = datetime.date.today().year

        # If the logo is for a non-current year, do not post news
        should_post_news = False if obj.year != year else True

        if should_post_news:
            headline_fmt = "New Holiday Logo by {}!"
            story_fmt = """
                {author} has submitted this logo for the <a href="/holiday/">Holiday Logo Contest</a>, thank you!<br><br>
                <img border="1" vspace="4" src="{logo.url}"></a>
            """
            news_post = News(
                user = request.user,
                headline = headline_fmt.format(obj.author),
                story = story_fmt.format(
                    author = obj.author,
                    logo = obj.logo,
                ),
            )

            news_post.save()

admin.site.register(HolidayLogo, HolidayLogoAdmin)
