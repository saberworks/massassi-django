import logging

from ninja import ModelSchema
from pydantic.typing import List, Optional
from pydantic import fields

from users.models import User
from .models import File, Game, Post, Project, Tag, TagType

# very restricted, just send back id and username
class UserOut(ModelSchema):
    class Config:
        model = User
        model_fields = ['id', 'username']


class GameOut(ModelSchema):
    image: Optional[str]

    class Config:
        model = Game
        model_fields = ['id', 'name', 'slug', 'description', 'image']


class TagTypeOut(ModelSchema):
    tag_type: str = fields.Field(None, alias='slug')

    class Config:
        model = TagType
        model_fields = ['id',]


class TagOut(ModelSchema):
    type: str = fields.Field(None, alias="type.slug")
    tag: str = fields.Field(None, alias='slug')

    class Config:
        model = Tag
        model_fields = ['id',]

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

class ProjectOut(ModelSchema):
    games: List[GameOut] = []
    tags: List[TagOut] = []
    image: Optional[str]

    class Config:
        model = Project
        model_fields = ['id', 'user', 'games', 'tags', 'name', 'slug', 'description', 'accent_color', 'image']


class PostOut(ModelSchema):
    image: Optional[str]

    class Config:
        model = Post
        model_fields = ['id', 'user', 'project', 'title', 'slug', 'text', 'image']

class FileOut(ModelSchema):
    image: Optional[str]

    class Config:
        model = File
        model_fields = ['id', 'user', 'project', 'name', 'version', 'description', 'file', 'image']
