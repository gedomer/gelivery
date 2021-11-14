from django.db.transaction import atomic
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from gelivery.core.models import Order, OrderItem
from gelivery.core.models.order import OrderStatus


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['food', 'quantity', 'amount']


class OrderListSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['pk', 'status', 'created_at', 'order_items']

    def get_order_items(self, obj):
        return OrderItemSerializer(obj.orderitem_set.all(), many=True).data


class OrderCreateSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['address', 'restaurant', 'order_items']

    def create(self, validated_data):
        with atomic():
            customer = self.context['user']
            order_items = validated_data.pop('order_items')
            new_order = Order(**validated_data, customer_id=customer.pk, status=OrderStatus.RECEIVED.value)
            new_order.save()

            items = [OrderItem(**item, order_id=new_order.pk) for item in order_items]
            OrderItem.objects.bulk_create(items, batch_size=1000)
        return new_order


class OrderCompleteSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField()

    class Meta:
        model = Order
        fields = ['order_id']

    def validate(self, attrs):
        order_already_completed = self.instance.status == OrderStatus.DELIVERED.value
        if order_already_completed:
            raise serializers.ValidationError({'detail': _('Order already delivered.')})
        return attrs

    def update(self, instance, validated_data):
        instance.status = OrderStatus.DELIVERED.value
        instance.save(update_fields=['status'])
        return instance
