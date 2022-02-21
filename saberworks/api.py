import logging
import re

from django.db import Error
from django.shortcuts import get_list_or_404, get_object_or_404
from ninja import Router, File as NinjaFile
from ninja.files import UploadedFile
from ninja.security import django_auth
from pydantic.typing import List, Optional

from .models import File, Game, Post, Project, Tag, TagType
from .schemas import FileOut, GameOut, PostOut, ProjectListOut, ProjectOut, TagOut, TagTypeOut
from .schemas import ProjectIn, NewProjectOut

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

###
## Get a list of projects
#
@router.get("/projects", response=List[ProjectListOut], auth=django_auth)
def get_projects(request):
    return get_list_or_404(Project, user=request.user)

###
## Get a single project
#
@router.get("/project/{project_id}", response=ProjectOut, auth=django_auth)
def get_project(request, project_id: int):
    return get_object_or_404(
        Project.objects
               .prefetch_related("tags__type")
               .select_related('user')
               .prefetch_related("games"),
        id=project_id, user=request.user)

###
## Create a new project
#
@router.post("/projects", response=NewProjectOut, auth=django_auth)
def add_project(request, payload: ProjectIn, image: Optional[UploadedFile] = NinjaFile(None)):
    project = payload.dict()

    games = project.pop('games', None)
    tags = project.pop('tags', None)

    project['user'] = request.user

    new_project = Project.objects.create(**project)

    messages = []

    # TODO this image handling allows putting any file as the image and django
    # model ImageField doesn't complain.  Need to do validation that
    # the thing uploaded is actually a valid image
    if image is not None:
        new_project.image = image
        new_project.save()

    if isinstance(games, list):
        try:
            [new_project.games.add(game) for game in games]
        except Error as error:
            if not re.search("foreign key constraint", str(error)):
                raise
            else:
                messages.append(get_friendly_invalid_fk_error_message(str(error)))

    if isinstance(tags, list):
        try:
            [new_project.tags.add(tag) for tag in tags]
        except Error as error:
            if not re.search("foreign key constraint", str(error)):
                raise
            else:
                messages.append(get_friendly_invalid_fk_error_message(str(error)))

    return { "project": new_project, "messages": messages }

# TODO:
# validate image uploads are actually images
# PUT edit project
# DELETE delete project

@router.get("/project/{project_id}/posts/", response=List[PostOut], auth=django_auth)
def get_posts_for_project(request, project_id: int):
    return get_list_or_404(Post, project_id=project_id, user=request.user)

@router.get("/project/{project_id}/posts/{post_id}", response=PostOut, auth=django_auth)
def get_post_for_project(request, project_id: int, post_id: int):
    return get_object_or_404(Post, project_id=project_id, id=post_id, user=request.user)

# TODO:
# POST add post (allow image upload somehow)
# PUT edit post
# DELETE delete post

@router.get("/project/{project_id}/files", response=List[FileOut], auth=django_auth)
def get_files_for_project(request, project_id):
    return get_list_or_404(File, project_id=project_id, user=request.user)

@router.get("/project/{project_id}/file/{file_id}", response=FileOut, auth=django_auth)
def get_file_for_project(request, project_id, file_id):
    return get_object_or_404(File, project_id=project_id, id=file_id, user=request.user)

# TODO:
# POST add file (allow image & file upload somehow)
# PUT edit file (allow replacement image? or delete image? or replace file? gah)
# DELETE delete file

# Given a databse error message from a foreign key constraint, extract the
# offending id and return it
def get_friendly_invalid_fk_error_message(error):
    result = re.search("\((\w+)\)=\((\d+)\)", error)

    if result is not None:
        [field, id] = result.groups()

        return "Error: {} is an invalid {}.".format(id, field)

    return "Some database error happened but I don't know what, sorry!"
