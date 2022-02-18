from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from .api import api
from screenshots import views as screenshots_views

urlpatterns = [
    path('', include('news.urls')),
    path('sotd/', include('sotd.urls')),
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    path('account/', include('users.urls')),
    path('levels/', include('levels.urls')),
    path('lotw/', include('lotw.urls')),
    path('holiday/', include('holiday.urls')),
    path('cgi-bin/screenshot.cgi', screenshots_views.old_cgi_screenshot_view),
    path('levels/files/thumbnails/<int:level_id>_<int:num>.<str:ext>', screenshots_views.thumbnail_view),
    path('levels/files/screenshots/<int:level_id>_<int:num>.<str:ext>', screenshots_views.screenshot_view),
]

# Text to put at the end of each page's <title>.
admin.site.site_title = 'Massassi Admin'

# Text to put in each page's <h1> (and above login form).
admin.site.site_header = 'Massassi Administration'

# Text to put at the top of the admin index page.
admin.site.index_title = 'Main'
