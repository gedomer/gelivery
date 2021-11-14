import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Food(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey('core.FoodCategory', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Food')
        verbose_name_plural = _('Foods')

    def __str__(self):
        return self.name
