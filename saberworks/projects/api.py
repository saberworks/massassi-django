import logging

from django.db.models.deletion import RestrictedError
from django.shortcuts import get_list_or_404, get_object_or_404
from ninja import Router, File as NinjaFile
from ninja.files import UploadedFile
from ninja.security import django_auth
from pydantic.typing import List, Optional

from saberworks.models import Project
from saberworks.schemas import ProjectListOut, ProjectOut, ProjectIn, NewProjectOut
from saberworks.util import gather_error_messages

from .forms import ProjectForm, ProjectEditForm, ProjectSetImageForm

logger = logging.getLogger(__name__)

router = Router(tags=['projects'], auth=django_auth)

#
# Get a list of projects
#
@router.get("/projects", response=List[ProjectListOut])
def get_projects(request):
    return get_list_or_404(Project, user=request.user)

#
# Get a single project
#
@router.get("/projects/{project_id}", response=ProjectOut)
def get_project(request, project_id: int):
    return get_object_or_404(
        Project.objects
            .prefetch_related("tags__type")
            .select_related('user')
            .prefetch_related("games"),
        id=project_id,
        user=request.user)

#
# Create a new project
#
@router.post("/projects", response=NewProjectOut)
def add_project(
    request,
    payload: ProjectIn,
    image: Optional[UploadedFile] = NinjaFile(None)
):
    project = payload.dict()

    project['user'] = request.user

    form = ProjectForm(project, { "image": image })

    if not form.is_valid():
        messages = gather_error_messages(form)

        return { "success": False, "messages": messages }

    new_project = form.save()

    return { "success": True, "project": new_project }

@router.post("/new", response=NewProjectOut)
def new_add_project(
    request,
    payload: ProjectIn,
    image: Optional[UploadedFile] = NinjaFile(None)
):
    project = payload.dict()

    games = project.pop('games', [])
    tags = project.pop('tags', [])

    project['user'] = request.user

    obj = Project(**project, image = image)
    obj.image.save("filename.jpg", image) # this will save project obj

    return { "success": True, "project": obj }

#
# Edit a project (not the image, that requires a separate request)
#
@router.put("/projects/{project_id}", response=NewProjectOut)
def edit_project(
    request,
    project_id: int,
    payload: ProjectIn,
):
    """
    Edit basic information about a project.  `POST` to
    `projects/{project_id}/image` to set the project image.
    """

    project = get_object_or_404(Project, id=project_id, user=request.user)

    data = payload.dict()

    form = ProjectEditForm(data, instance=project)

    if not form.is_valid():
        messages = gather_error_messages(form)

        return { "success": False, "messages": messages }

    edited_project = form.save()

    return { "success": True, "project": edited_project }

#
# Set a project image
#
@router.post("/projects/{project_id}/image", response=NewProjectOut)
def set_project_image(request, project_id: int, image: UploadedFile):
    """
    Set the project image.  If you want to delete the project image, send a
    `DELETE` request to `/projects/{project_id}/image`.
    """
    project = get_object_or_404(Project, id=project_id, user=request.user)

    form = ProjectSetImageForm(None, { "image": image }, instance=project)

    if not form.is_valid():
        messages = gather_error_messages(form)

        return { "success": False, "messages": messages }

    new_project = form.save()

    return { "success": True, "project": new_project }

#
# Delete a project image
#
@router.delete("/projects/{project_id}/image", response=NewProjectOut)
def delete_project_image(request, project_id: int):
    """
    Delete the image associated with a project (does not delete the project).
    """

    project = get_object_or_404(Project, id=project_id, user=request.user)

    project.image = None

    project.save()

    return { "success": True, "project": project }

#
# Delete a project
#
@router.delete("/projects/{project_id}")
def delete_project(request, project_id: int):
    """
    Deletes an entire project.  The project must not have any associated
    posts or files (delete them separately first).

    WARNING: This is permanent, there is no recovery.
    """

    project = get_object_or_404(Project, id=project_id, user=request.user)

    try:
        project.delete()
    except RestrictedError as error:
        message = "This {} associated with this project prevents deletion: {}"
        messages = []

        for item in error.restricted_objects:
            classname = item.__class__.__name__
            messages.append(message.format(classname, str(item)))

        return { "success": False, "messages": messages }

    return { "success": True }
