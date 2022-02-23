import logging

from django.db.models.deletion import RestrictedError
from django.shortcuts import get_list_or_404, get_object_or_404
from ninja import Router, File as NinjaFile
from ninja.files import UploadedFile
from ninja.security import django_auth
from pydantic.typing import List, Optional

from saberworks.models import File, Project
from saberworks.schemas import FileOut, FileIn, NewFileOut
from saberworks.util import gather_error_messages

from .forms import FileForm, FileEditForm, FileSetImageForm

logger = logging.getLogger(__name__)

router = Router(tags=['files'], auth=django_auth)

#
# Get list of files in project
#
@router.get("/projects/{project_id}/files", response=List[FileOut])
def get_files_for_project(request, project_id):
    return get_list_or_404(File, project_id=project_id, user=request.user)

#
# Get a single file from project
#
@router.get("/projects/{project_id}/file/{file_id}", response=FileOut)
def get_file_for_project(request, project_id, file_id):
    return get_object_or_404(
        File, project_id=project_id, id=file_id, user=request.user
    )

#
# Add new file to project
#
@router.post("/projects/{project_id}/files", response=NewFileOut)
def add_file(
    request,
    project_id: int,
    payload: FileIn,
    uploaded_file: UploadedFile,
    uploaded_image: Optional[UploadedFile] = NinjaFile(None)
):
    project = get_object_or_404(Project, id=project_id, user=request.user)

    file = payload.dict()

    file['user'] = request.user
    file['project'] = project.id

    form = FileForm(file, { "file": uploaded_file, "image": uploaded_image })

    if not form.is_valid():
        messages = gather_error_messages(form)

        return { "success": False, "messages": messages }

    new_file = form.save()

    return { "success": True, "file": new_file }

#
# Edit a file (not the image, that requires a separate request)
#
@router.put("/projects/{project_id}/files/{file_id}", response=NewFileOut)
def edit_file(
    request,
    project_id: int,
    file_id: int,
    payload: FileIn,
):
    """
    Edit a file.  `POST` to `projects/{project_id}/files/{file_id}/image` to
    set the file image.

    Note: only name, version, and description can be changed (and image if you
    follow the instructions above).  If you want to change the actual file,
    you should delete this file and upload a new one.
    """

    file = get_object_or_404(
        File, id=file_id, project_id=project_id, user=request.user
    )

    data = payload.dict()

    form = FileEditForm(data, instance=file)

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
