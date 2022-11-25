import logging

from ninja import Schema, ModelSchema
from ninja.files import UploadedFile
from pydantic.typing import List, Optional
from pydantic import fields

from users.models import User
from .models import File, Game, Post, Project, Screenshot, Tag, TagType

# UserOut schema is very restricted, just send back id and username
class UserOut(ModelSchema):
    class Config:
        model = User
        model_fields = ['id', 'username']


#
# Game Schemas
#

class GameOut(ModelSchema):
    image: Optional[str]

    class Config:
        model = Game
        model_fields = ['id', 'name', 'slug', 'description', 'image', 'color']


#
# Tag Type Schemas
#

class TagTypeOut(ModelSchema):
    tag_type: str = fields.Field(None, alias='slug')

    class Config:
        model = TagType
        model_fields = ['id', 'color']

#
# Tag Schemas
#

class TagOut(ModelSchema):
    type: str = fields.Field(None, alias="type.slug")
    tag: str = fields.Field(None, alias='slug')

    class Config:
        model = Tag
        model_fields = ['id', 'color']


#
# Project Schemas
#

# This is here so one can request a list of projects and not cause a bunch of
# cascading queries.  It's similar to ProjectOut below except that all the
# foreign keys will be returned directly instead of looking up the associated
# values. (and it doesn't look up anything in many-to-many relationships -- so
# no games or tags)
class ProjectListOut(ModelSchema):
    games: List[GameOut] = []
    tags: List[TagOut] = []
    image: Optional[str]

    class Config:
        model = Project
        model_fields = [
            'id', 'user', 'name', 'slug', 'description', 'accent_color',
            'created_at',
        ]

class ProjectIn(ModelSchema):
    games: List[int] = [] # list of game IDs
    tags: List[int] = []  # list of tag IDs

    class Config:
        model = Project
        model_fields = ['games', 'tags', 'name', 'description', 'accent_color']

class ProjectOut(ModelSchema):
    games: List[GameOut] = []
    tags: List[TagOut] = []
    image: Optional[str]

    class Config:
        model = Project
        model_fields = [
            'id', 'user', 'name', 'slug', 'description', 'accent_color',
            'created_at'
        ]

class NewProjectOut(Schema):
    success: bool
    project: Optional[ProjectOut] = None
    messages: Optional[List[str]] = []


#
# Post Schemas
#

class PostIn(ModelSchema):
    class Config:
        model = Post
        model_fields = ['title', 'text']

class PostOut(ModelSchema):
    image: Optional[str]

    class Config:
        model = Post
        model_fields = ['id', 'user', 'project', 'title', 'slug', 'text', 'image', 'created_at']

class NewPostOut(Schema):
    success: bool
    post: Optional[PostOut] = None
    messages: Optional[List[str]] = []


#
# File Schemas
#

class FileIn(ModelSchema):
    class Config:
        model = File
        model_fields = ['title', 'version', 'description']

class FileOut(ModelSchema):
    image: Optional[str]

    class Config:
        model = File
        model_fields = [
            'id', 'user', 'project', 'title', 'name', 'version', 'description',
            'file', 'file_size', 'file_hash', 'image', 'created_at'
        ]

class StagedFileOut(ModelSchema):
    image: Optional[str]
    file: Optional[str]

    class Config:
        model = File
        model_fields = [
            'id', 'user', 'project', 'title', 'version', 'description',
            'created_at'
        ]

class NewStagedFileOut(Schema):
    success: bool
    file: Optional[StagedFileOut] = None
    messages: Optional[List[str]]

class NewFileOut(Schema):
    success: bool
    file: Optional[FileOut] = None
    messages: Optional[List[str]] = []

#
# Screenshot Schemas
#
class ScreenshotOut(ModelSchema):
    class Config:
        model = Screenshot
        model_fields = ['id', 'user', 'project', 'image', 'created_at']

class NewScreenshotOut(Schema):
    success: bool
    screenshot: ScreenshotOut
    messages: Optional[List[str]] = []
