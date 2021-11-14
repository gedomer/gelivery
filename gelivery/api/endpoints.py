
import json

import redis
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView as BaseAPIView

from gelivery.core.models import Order
from .serializers import (OrderCompleteSerializer, OrderCreateSerializer,
                          OrderListSerializer)


class Endpoint(BaseAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)


class OrderListEndpoint(Endpoint):

    def get(self, request):
        orders = request.user.customer.order_set.all()

        order_status = self.request.query_params.get('status')
        if order_status:
            orders = orders.filter(status=order_status)
        orders = orders.prefetch_related('orderitem_set')

        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data, status=200)


class OrderCreateEndpoint(Endpoint):

    def _publish_message(self, channel_name, data):
        json_data = json.dumps(data)
        redis_instance = redis.StrictRedis(host=settings.REDIS_HOSTNAME)
        redis_instance.publish(channel_name, json_data)

    def post(self, request):
        serializer = OrderCreateSerializer(
            data=request.data, context={'user': self.request.user})
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        new_order = serializer.save()
        body = {
            'message': 'order_created',
            'order_id': str(new_order.pk)
        }
        self._publish_message('orders', body)
        return Response(body, status=201)


class OrderCompleteEndpoint(Endpoint):

    permission_classes = (AllowAny,)
    authentication_classes = []

    def post(self, request):
        order = get_object_or_404(Order, pk=request.data.get('order_id'))
        serializer = OrderCompleteSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data, status=201)
        return Response(serializer.errors, status=400)
