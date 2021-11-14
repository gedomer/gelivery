import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class FoodCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(max_length=1000)

    class Meta:
        verbose_name = _('Food Category')
        verbose_name_plural = _('Food Categories')

    def __str__(self):
        return self.name
