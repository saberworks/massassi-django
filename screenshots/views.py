import logging
import re

from django.http.response import Http404
from django.shortcuts import redirect

from levels.models import Level

#
# This app exists to redirect old-school screenshot and thumbnail URLs to the
# new django-based stuff.  It didn't seem possible to use a static redirect
# (like in nginx conf or something) because screenshot URLs change when images
# are updated (unlike the old system which just overwrote the screenshot files),
# and also thumbnail urls are unpredictable because they're generated
# automatically and use some sort of hasing mechanism.
#
# Why do I care about old screenshot and thumbnail urls?  Because in the "old
# news" section there are a zillion links over 20 years using the old urls and
# without this, the old news screenshot embeds are broken.
#
# to make links work:
# /cgi-bin/screenshot.cgi?levels/files/screenshots/3136_1.jpg
#
# to make embedded screenshots/thumbnails work:
# /levels/files/thumbnails/3136_1.jpg
# /levels/files/screenshots/3136_1.jpg
#

logger = logging.getLogger(__name__)

def old_cgi_screenshot_view(request):
    # django apparently doesn't allow me to access the raw query string
    # (like in this case '?levels/files/screenshots/3136_1.jpg')
    path = request.get_full_path()

    ss_pattern = re.compile(r'(\d+)_(\d+)\.\w{3,4}$')
    res = re.search(ss_pattern, path)

    level_id = res.group(1)
    num = res.group(2)

    if level_id and num:
        return redirect(get_screenshot_url(level_id, num))
    else:
        raise Http404("level screenshot can't be found")

def screenshot_view(request, level_id, num, ext):
    return redirect(get_screenshot_url(level_id, num))

def thumbnail_view(request, level_id, num, ext):
    return redirect(get_thumbnail_url(level_id, num))

def get_screenshot_url(level_id, num):
    level = Level.objects.get(pk=level_id)
    method = "screenshot_" + str(num)
    shot = getattr(level, method)
    return shot.url

def get_thumbnail_url(level_id, num):
    level = Level.objects.get(pk=level_id)
    method = "thumbnail_" + str(num)
    thumb = getattr(level, method)
    return thumb.url
