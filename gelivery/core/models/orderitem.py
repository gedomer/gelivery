from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderItem(models.Model):
    order = models.ForeignKey('core.Order', on_delete=models.CASCADE)
    food = models.ForeignKey('core.Food', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=15, decimal_places=6)

    class Meta:
        verbose_name = _('Order Item')
        verbose_name_plural = _('Order Items')
