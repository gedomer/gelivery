import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(max_length=1000)
    city = models.CharField(max_length=100)

    class Meta:
        verbose_name = _('Restaurant')
        verbose_name_plural = _('Restaurants')

    def __str__(self):
        return f'{self.name} - {self.city}'
