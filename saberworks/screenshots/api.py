import logging

from django.db.models.deletion import RestrictedError
from django.shortcuts import get_list_or_404, get_object_or_404
from ninja import Router, File as NinjaFile
from ninja.files import UploadedFile
from ninja.security import django_auth
from pydantic.typing import List, Optional

from saberworks.models import Project, Screenshot
from saberworks.schemas import NewScreenshotOut, ScreenshotOut
from saberworks.util import gather_error_messages

from .forms import AddScreenshotForm

logger = logging.getLogger(__name__)

router = Router(tags=['screenshots'], auth=django_auth)

#
# Get a list of screenshots in a project
#
@router.get("/projects/{project_id}/screenshots", response=List[ScreenshotOut])
def get_screenshots_for_project(request, project_id: int):
    return get_list_or_404(Screenshot, project_id=project_id, user=request.user)

#
# Add a project screenshot
#
@router.post("/projects/{project_id}/screenshots", response=NewScreenshotOut)
def add_screenshot(request, project_id: int, image: UploadedFile):
    """
    Add a screenshot to a project.  If you want to delete the screenshot, send
    a `DELETE` request to `/projects/{project_id}/screenshots/{screenshot_id}`.
    """
    project = get_object_or_404(Project, id=project_id, user=request.user)

    data = {
        "user": request.user,
        "project": project.id,
    }

    form = AddScreenshotForm(data, { "image": image })

    if not form.is_valid():
        messages = gather_error_messages(form)

        return { "success": False, "messages": messages }

    new_screenshot = form.save()

    return { "success": True, "screenshot": new_screenshot }
