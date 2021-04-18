from functools import lru_cache

from django.core.exceptions import ObjectDoesNotExist

from levels.models import Level
from users.models import User


@lru_cache(maxsize=None)
def get_level(level_id):
    try:
        return Level.objects.get(pk=level_id)
    except ObjectDoesNotExist:
        return None


@lru_cache(maxsize=None)
def get_user(user_id):
    try:
        return User.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        return None
