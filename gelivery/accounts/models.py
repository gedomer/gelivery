from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserStatus(models.TextChoices):
    DELETED = 'deleted', _('Deleted')
    ACTIVE = 'active', _('Active')


class User(AbstractUser):
    language = models.CharField(
        choices=settings.LANGUAGES,
        max_length=10,
        default=settings.LANGUAGE_CODE
    )
    status = models.CharField(
        choices=UserStatus.choices,
        max_length=50,
        default=UserStatus.ACTIVE
    )
