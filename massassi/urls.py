from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('sotd/', include('sotd.urls')),
    path('admin/', admin.site.urls),
    path('account/', include('users.urls')),
]

# Text to put at the end of each page's <title>.
admin.site.site_title = 'Massassi Admin'

# Text to put in each page's <h1> (and above login form).
admin.site.site_header = 'Massassi Administration'

# Text to put at the top of the admin index page.
admin.site.index_title = 'Main'

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
