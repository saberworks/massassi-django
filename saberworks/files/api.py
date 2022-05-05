import logging
import pprint

from django.db.models.deletion import RestrictedError
from django.shortcuts import get_list_or_404, get_object_or_404
from ninja import Router, File as NinjaFile
from ninja.files import UploadedFile
from ninja.security import django_auth
from pydantic.typing import List, Optional

from saberworks.models import File, Project
from saberworks.schemas import FileOut, FileIn, NewFileOut, NewStagedFileOut
from saberworks.util import gather_error_messages

from .forms import FileForm, FileEditForm, FileSetFileForm, FileSetImageForm, StageFileForm

logger = logging.getLogger(__name__)

router = Router(tags=['files'], auth=django_auth)

#
# Get list of files in project
#
@router.get("/projects/{project_id}/files", response=List[FileOut])
def get_files_for_project(request, project_id):
    return get_list_or_404(
        File.objects,
        project_id=project_id,
        user=request.user,
    )

#
# Get a single file from project
#
@router.get("/projects/{project_id}/file/{file_id}", response=FileOut)
def get_file_for_project(request, project_id, file_id):
    return get_object_or_404(
        File, project_id=project_id, id=file_id, user=request.user
    )

#
# Stage a file
#
# This means a request comes in as a new file upload for a specific project.
# The only metadata we have is the project_id and the user_id (from the
# request).  We insert a blank/dummy row to get a file_id and return that.
#
@router.post("/projects/{project_id}/files.stage", response=NewStagedFileOut)
def stage_file(request, project_id: int):
    project = get_object_or_404(Project, id=project_id, user=request.user)

    file_data = {
        "project": project_id,
        "user": request.user,
        "title": "TEMP",
        "version": "TEMP",
        "description": "TEMP",
        "image": None,
        "file": None,
    }

    form = StageFileForm(file_data)

    if not form.is_valid():
        messages = gather_error_messages(form)

        return { "success": False, "messages": messages }

    staged_file = form.save()

    return { "success": True, "file": staged_file }

@router.post("/projects/{project_id}/files.upload/{file_id}", response=NewFileOut)
def upload_file(request, project_id: int, file_id: int, file: UploadedFile):
    file_row = get_object_or_404(File, project=project_id, id=file_id, user=request.user)

    form = FileSetFileForm(None, { "file": file }, instance=file_row)

    if not form.is_valid():
        messages = gather_error_messages(form)

        return { "success": False, "messages": messages }

    staged_file = form.save()

    return { "success": True, "file": staged_file }

#
# Add new file to project
#
@router.post("/projects/{project_id}/files", response=NewFileOut)
def add_file(
    request,
    project_id: int,
    payload: FileIn,
    file: UploadedFile,
    image: Optional[UploadedFile] = NinjaFile(None)
):
    project = get_object_or_404(Project, id=project_id, user=request.user)

    body = payload.dict()

    body['user'] = request.user
    body['project'] = project.id

    form = FileForm(body, { "file": file, "image": image })

    if not form.is_valid():
        messages = gather_error_messages(form)

        return { "success": False, "messages": messages }

    new_file = form.save()

    return { "success": True, "file": new_file }

#
# Edit a file.  Note this is a POST not a PUT because web server doesn't accept
# request BODY on PUT requests.
#
@router.post("/projects/{project_id}/files/{file_id}", response=NewFileOut)
def edit_file(
    request,
    project_id: int,
    file_id: int,
    payload: FileIn,
    image: Optional[UploadedFile] = NinjaFile(None),
):
    file = get_object_or_404(
        File, id=file_id, project_id=project_id, user=request.user
    )

    data = payload.dict()

    form = FileEditForm(data, { "image": image }, instance=file)

    if not form.is_valid():
        messages = gather_error_messages(form)

        return { "success": False, "messages": messages }

    edited_file = form.save()

    return { "success": True, "file": edited_file }

#
# Set a file image
#
@router.post("/projects/{project_id}/files/{file_id}/image", response=NewFileOut)
def set_file_image(request, project_id: int, file_id: int, image: UploadedFile):
    """
    Set the file image.  If you want to delete the file image, send a
    `DELETE` request to `/projects/{project_id}/files/{file_id}/image`.
    """

    file = get_object_or_404(
        File, id=file_id, project_id=project_id, user=request.user
    )

    form = FileSetImageForm(None, { "image": image }, instance=file)

    if not form.is_valid():
        messages = gather_error_messages(form)

        return { "success": False, "messages": messages }

    edited_file = form.save()

    return { "success": True, "file": edited_file }

#
# Delete a file image
#
@router.delete("/projects/{project_id}/files/{file_id}/image", response=NewFileOut)
def delete_file_image(request, project_id: int, file_id: int):
    """
    Delete the image associated with a file (does not delete the file).
    """

    file = get_object_or_404(
        File, id=file_id, project_id=project_id, user=request.user
    )

    file.image = None

    file.save()

    return { "success": True, "file": file }

#
# Delete a file
#
@router.delete("/projects/{project_id}/files/{file_id}")
def delete_file(request, project_id: int, file_id: int):
    """
    Deletes an entire file.

    WARNING: This is permanent, there is no recovery.
    """

    file = get_object_or_404(
        File, id=file_id, project_id=project_id, user=request.user
    )

    # currently there are no associated objects/foreign keys for files, but
    # I guess there might be some day?
    try:
        file.delete()
    except RestrictedError as error:
        message = "This {} associated with this file prevents deletion: {}"
        messages = []

        for item in error.restricted_objects:
            classname = item.__class__.__name__
            messages.append(message.format(classname, str(item)))

        return { "success": False, "messages": messages }

    return { "success": True }
