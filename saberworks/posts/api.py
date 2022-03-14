import logging

from django.db.models.deletion import RestrictedError
from django.shortcuts import get_list_or_404, get_object_or_404
from ninja import File as NinjaFile
from ninja import Router
from ninja.files import UploadedFile
from ninja.security import django_auth
from pydantic.typing import List, Optional

from saberworks.models import Post, Project
from saberworks.schemas import NewPostOut, PostIn, PostOut
from saberworks.util import gather_error_messages

from .forms import PostForm, PostEditForm, PostSetImageForm

logger = logging.getLogger(__name__)

router = Router(tags=['posts'], auth=django_auth)

#
# Get a list of posts for a project
#
@router.get("/projects/{project_id}/posts", response=List[PostOut])
def get_posts_for_project(request, project_id: int):
    return get_list_or_404(Post, project_id=project_id, user=request.user)

#
# Get a single post for a project
#
@router.get("/projects/{project_id}/posts/{post_id}", response=PostOut)
def get_post_for_project(request, project_id: int, post_id: int):
    return get_object_or_404(
        Post, project_id=project_id, id=post_id, user=request.user
    )

#
# Create a new post
#
@router.post("/projects/{project_id}/posts", response=NewPostOut)
def add_post(
    request,
    project_id: int,
    payload: PostIn,
):
    """
    Create a new post without a post image.  This must be submitted
    using content-type: application/json.  Note: you can use the
    method that adds a post with an image even if you don't have an image.
    """
    project = get_object_or_404(Project, id=project_id, user=request.user)

    post = payload.dict()

    post['user'] = request.user
    post['project'] = project.id

    form = PostForm(post)

    if not form.is_valid():
        messages = gather_error_messages(form)

        return { "success": False, "messages": messages }

    new_post = form.save()

    return { "success": True, "post": new_post }

#
# Create a new post with image
#
@router.post("/projects/{project_id}/posts.with_image", response=NewPostOut)
def add_post_with_image(
    request,
    project_id: int,
    payload: PostIn,
    image: Optional[UploadedFile] = NinjaFile(None)
):
    """
    Create a new post, include a post image.  This must be submitted
    using enctype=multipart/form-data.  Note: you can use this method even
    if your post doesn't have an image, just leave the field blank.  But it
    still must be submitted as form-data.
    """
    project = get_object_or_404(Project, id=project_id, user=request.user)

    post = payload.dict()

    post['user'] = request.user
    post['project'] = project.id

    form = PostForm(post, { "image": image })

    if not form.is_valid():
        messages = gather_error_messages(form)

        return { "success": False, "messages": messages }

    new_post = form.save()

    return { "success": True, "post": new_post }

#
# Edit a post without an image
#
@router.put("/projects/{project_id}/posts/{post_id}", response=NewPostOut)
def edit_post(
    request,
    project_id: int,
    post_id: int,
    payload: PostIn,
):
    post = get_object_or_404(
        Post, id=post_id, project_id=project_id, user=request.user
    )

    data = payload.dict()

    form = PostEditForm(data, instance=post)

    if not form.is_valid():
        messages = gather_error_messages(form)

        return { "success": False, "messages": messages }

    edited_post = form.save()

    return { "success": True, "post": edited_post }

#
# Edit a post with an image
#
@router.post("/projects/{project_id}/posts/{post_id}", response=NewPostOut)
def edit_post_with_image(
    request,
    project_id: int,
    post_id: int,
    payload: PostIn,
    image: Optional[UploadedFile] = NinjaFile(None)
):
    post = get_object_or_404(
        Post, id=post_id, project_id=project_id, user=request.user
    )

    data = payload.dict()

    form = PostEditForm(data, { "image": image }, instance=post)

    if not form.is_valid():
        messages = gather_error_messages(form)

        return { "success": False, "messages": messages }

    edited_post = form.save()

    return { "success": True, "post": edited_post }

#
# Set a post image
#
@router.post("/projects/{project_id}/posts/{post_id}/image", response=NewPostOut)
def set_post_image(request, project_id: int, post_id: int, image: UploadedFile):
    """
    Set the post image.  If you want to delete the post image, send a
    `DELETE` request to `/projects/{project_id}/posts/{post_id}/image`.
    """
    post = get_object_or_404(
        Post, id=post_id, project_id=project_id, user=request.user
    )

    form = PostSetImageForm(None, { "image": image }, instance=post)

    if not form.is_valid():
        messages = gather_error_messages(form)

        return { "success": False, "messages": messages }

    edited_post = form.save()

    return { "success": True, "post": edited_post }

#
# Delete a post image
#
@router.delete("/projects/{project_id}/posts/{post_id}/image", response=NewPostOut)
def delete_post_image(request, project_id: int, post_id: int):
    """
    Delete the image associated with a post (does not delete the post).
    """

    post = get_object_or_404(
        Post, id=post_id, project_id=project_id, user=request.user
    )

    post.image = None

    post.save()

    return { "success": True, "post": post }

#
# Delete a post
#
@router.delete("/projects/{project_id}/posts/{post_id}")
def delete_post(request, project_id: int, post_id: int):
    """
    Deletes an entire post.

    WARNING: This is permanent, there is no recovery.
    """

    post = get_object_or_404(
        Post, id=post_id, project_id=project_id, user=request.user
    )

    # currently there are no associated objects/foreign keys for posts, but
    # I guess there might be some day?
    try:
        post.delete()
    except RestrictedError as error:
        message = "This {} associated with this post prevents deletion: {}"
        messages = []

        for item in error.restricted_objects:
            classname = item.__class__.__name__
            messages.append(message.format(classname, str(item)))

        return { "success": False, "messages": messages }

    return { "success": True }
