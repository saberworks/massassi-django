import logging

from ninja import Schema, ModelSchema
from ninja.files import UploadedFile
from pydantic.typing import List, Optional
from pydantic import fields

from users.models import User
from .models import File, Game, Post, Project, Tag, TagType

# UserOut schema is very restricted, just send back id and username
class UserOut(ModelSchema):
    class Config:
        model = User
        model_fields = ['id', 'username']


###
## Game Schemas
#

class GameOut(ModelSchema):
    image: Optional[str]

    class Config:
        model = Game
        model_fields = ['id', 'name', 'slug', 'description', 'image']


###
## Tag Type Schemas
#

class TagTypeOut(ModelSchema):
    tag_type: str = fields.Field(None, alias='slug')

    class Config:
        model = TagType
        model_fields = ['id',]

###
## Tag Schemas
#

class TagOut(ModelSchema):
    type: str = fields.Field(None, alias="type.slug")
    tag: str = fields.Field(None, alias='slug')

    class Config:
        model = Tag
        model_fields = ['id',]


###
## Project Schemas
#

# This is here so one can request a list of projects and not cause a bunch of
# cascading queries.  It's similar to ProjectOut below except that all the
# foreign keys will be returned directly instead of looking up the associated
# values. (and it doesn't look up anything in many-to-many relationships -- so
# no games or tags)
class ProjectListOut(ModelSchema):
    image: Optional[str]

    class Config:
        model = Project
        model_fields = ['id', 'user', 'name', 'slug', 'description', 'accent_color', 'image']

class ProjectIn(ModelSchema):
    games: List[int] = [] # list of game IDs
    tags: List[int] = []  # list of tag IDs
    image: Optional[UploadedFile] = None

    class Config:
        model = Project
        model_fields = ['games', 'tags', 'name', 'description', 'accent_color', 'image']

class ProjectOut(ModelSchema):
    games: List[GameOut] = []
    tags: List[TagOut] = []
    image: Optional[str]

    class Config:
        model = Project
        model_fields = ['id', 'user', 'games', 'tags', 'name', 'slug', 'description', 'accent_color', 'image']

class NewProjectOut(Schema):
    project: ProjectOut
    messages: Optional[List[str]] = []


###
## Post Schemas
#

class PostOut(ModelSchema):
    image: Optional[str]

    class Config:
        model = Post
        model_fields = ['id', 'user', 'project', 'title', 'slug', 'text', 'image']


###
## File Schemas
#

class FileOut(ModelSchema):
    image: Optional[str]

    class Config:
        model = File
        model_fields = ['id', 'user', 'project', 'name', 'version', 'description', 'file', 'image']
