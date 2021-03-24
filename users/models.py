from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.utils import timezone

from .validators import OurUnicodeUsernameValidator

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        'username',
        blank=False,
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and ./+/-/_ only.',
        validators=[OurUnicodeUsernameValidator()],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )

    email = models.EmailField('email_address', blank=False)

    is_staff = models.BooleanField(
        'is_staff',
        default=False,
        help_text='If true, allows admin login.',
    )

    is_active = models.BooleanField(
        'is_active',
        default=True,
        help_text=(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )

    date_joined = models.DateTimeField('date_joined', null=True, default=timezone.now)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)
    objects = UserManager()

    def __str__(self):
        return "{} ({})".format(self.username, self.id)
