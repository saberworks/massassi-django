import logging

from django.shortcuts import get_list_or_404, get_object_or_404
from ninja import Router
from ninja.security import django_auth
from pydantic.typing import List

from .models import File, Game, Post, Project, Tag, TagType
from .schemas import FileOut, GameOut, PostOut, ProjectListOut, ProjectOut, TagOut, TagTypeOut

logger = logging.getLogger(__name__)

router = Router()

@router.get("/games", response=List[GameOut])
def get_games(request):
    return get_list_or_404(Game)

@router.get("/tag_types", response=List[TagTypeOut])
def get_tag_types(request):
    return get_list_or_404(TagType)

@router.get("/tags", response=List[TagOut])
def get_tags(request):
    return get_list_or_404(Tag.objects.select_related('type'))

#
# The routes below here are specific to users, only return items owned by the
# logged in user
#

@router.get("/projects", response=List[ProjectListOut], auth=django_auth)
def get_projects(request):
    return get_list_or_404(Project, user=request.user)

@router.get("/project/{project_id}", response=ProjectOut, auth=django_auth)
def get_project(request, project_id: int):
    return get_object_or_404(
        Project.objects
               .prefetch_related("tags__type")
               .select_related('user')
               .prefetch_related("games"),
        id=project_id, user=request.user)

# TODO:
# POST add project (allow specifying of tags, games)
# PUT edit project
# DELETE delete project

@router.get("/project/{project_id}/posts/", response=List[PostOut])
def get_posts_for_project(request, project_id: int):
    return get_list_or_404(Post, project_id=project_id, user=request.user)

@router.get("/project/{project_id}/posts/{post_id}", response=PostOut)
def get_post_for_project(request, project_id: int, post_id: int):
    return get_object_or_404(Post, project_id=project_id, id=post_id, user=request.user)

# TODO:
# POST add post (allow image upload somehow)
# PUT edit post
# DELETE delete post

@router.get("/project/{project_id}/files", response=List[FileOut])
def get_files_for_project(request, project_id):
    return get_list_or_404(File, project_id=project_id, user=request.user)

@router.get("/project/{project_id}/file/{file_id}", response=FileOut)
def get_file_for_project(request, project_id, file_id):
    return get_object_or_404(File, project_id=project_id, id=file_id, user=request.user)

# TODO:
# POST add file (allow image & file upload somehow)
# PUT edit file (allow replacement image? or delete image? or replace file? gah)
# DELETE delete file
