import logging

from django.conf import settings
from django.shortcuts import get_list_or_404, get_object_or_404
from django.urls import reverse
from ninja import ModelSchema, Router
from pydantic.typing import List, Optional

from levels.models import Level, LevelCategory

logger = logging.getLogger(__name__)

class LevelCategoryOut(ModelSchema):
    class Config:
        model = LevelCategory
        model_fields = [
            'id', 'path', 'name', 'description', 'game', 'enable_3dpreview'
        ]

class LevelOut(ModelSchema):
    screenshot_1_url: Optional[str]
    screenshot_2_url: Optional[str]
    download_url: str
    level_url: str
    category_name: str

    class Config:
        model = Level
        model_fields = [
            'id', 'category', 'name', 'description', 'author',
            'dl_count', 'comment_count', 'rate_count', 'rating',
            'created_at']


router = Router()

@router.get("/categories", response=List[LevelCategoryOut], tags=['levels'])
def get_categories(request):
    return get_list_or_404(LevelCategory)

@router.get("/{str:category}", response=List[LevelOut], tags=['levels'])
def get_levels(request, category: str, order_by: str = "name"):
    cat = get_object_or_404(LevelCategory, path=category)
    cat_name = cat.name

    allowed_order_strings = {
        "author": "author",
        "name": "name",
        "created_at": "created_at",
        "dl_count": "dl_count",
        "rating": "rating",
    }

    order_by = allowed_order_strings.get(order_by, "name")

    levels = Level.objects \
                  .filter(category=cat) \
                  .order_by(order_by)

    # intentional closure around `request` and `cat_name`
    def add_extra(obj):
        obj.screenshot_1_url = screenshot_url(request, obj.screenshot_1)
        obj.screenshot_2_url = screenshot_url(request, obj.screenshot_2)
        obj.download_url = download_url(request, obj.file.url)
        obj.category_name = cat_name
        obj.level_url = level_url(request, obj.id)

        return obj

    return list(map(add_extra, levels))



#
# For some reason, screenshots do NOT store "/media/" in their db field, but
# the file fields DO.  What the heck?
#

media_prefix = settings.MEDIA_URL

def screenshot_url(request, screenshot):
    return request.build_absolute_uri(media_prefix) + str(screenshot) if screenshot else ""

def download_url(request, path):
    return request.build_absolute_uri(str(path))

def level_url(request, level_id):
    return request.build_absolute_uri(reverse('levels:level', args=[level_id]))
