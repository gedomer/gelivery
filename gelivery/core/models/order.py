import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class OrderStatus(models.TextChoices):
    CANCELLED = 'cancelled', _('Cancelled')
    RECEIVED = 'received', _('Received')
    ON_THE_WAY = 'on-the-way', _('On the way')
    DELIVERED = 'delivered', _('Delivered')


class Order(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('core.Customer', on_delete=models.PROTECT)
    restaurant = models.ForeignKey('core.Restaurant', on_delete=models.PROTECT)
    status = models.CharField(
        choices=OrderStatus.choices,
        max_length=20,
        default=OrderStatus.RECEIVED.value
    )
    address = models.TextField(max_length=1000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')
