import logging

from django.shortcuts import get_list_or_404
from ninja.router import Router
from pydantic.typing import List

from .models import Game, Tag, TagType
from .schemas import GameOut, TagOut, TagTypeOut

from .files.api import router as files_router
from .posts.api import router as posts_router
from .projects.api import router as projects_router

logger = logging.getLogger(__name__)

router = Router()

# Note: the following 3 routers define routes under /projects
router.add_router('/', projects_router)
router.add_router('/', posts_router)
router.add_router('/', files_router)

@router.get("/games", response=List[GameOut], tags=['games'])
def get_games(request):
    return get_list_or_404(Game)

@router.get("/tag_types", response=List[TagTypeOut], tags=['tag_types'])
def get_tag_types(request):
    return get_list_or_404(TagType)

@router.get("/tags", response=List[TagOut], tags=['tags'])
def get_tags(request):
    return get_list_or_404(Tag.objects.select_related('type'))
