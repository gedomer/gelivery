import uuid
from unittest.mock import patch

from django.urls import reverse
from rest_framework.test import APITestCase as BaseAPITestCase

from gelivery.core.factories import (CustomerFactory, FoodFactory, OrderFactory,
                                     OrderItemFactory, RestaurantFactory)
from gelivery.core.models.order import OrderStatus

from .serializers import OrderItemSerializer


class EndpointTestCase(BaseAPITestCase):

    def _get_token(self, as_user):
        if as_user:
            as_user = getattr(as_user, 'user', as_user)
            return as_user.auth_token.key

    def get(self, path, as_user=None, **kwargs):
        key = self._get_token(as_user)
        return self.client.get(path, HTTP_AUTHORIZATION=f'Token {key}', **kwargs)

    def post(self, path, payload=None, as_user=None, **kwargs):
        key = self._get_token(as_user)
        return self.client.post(
            path,
            data=payload,
            format='json',
            HTTP_AUTHORIZATION=f'Token {key}',
            HTTP_CONTENT_TYPE='application/json; charset=utf-8',
            **kwargs
        )


class OrderListTests(EndpointTestCase):

    def setUp(self):
        self.customer = CustomerFactory()
        self.path = reverse('api:order-list')

    def test_get_order_list(self):
        """GET /api/v1/orders/ returns a list of orders"""

        OrderFactory(status=OrderStatus.CANCELLED.value, customer=self.customer)
        OrderFactory(status=OrderStatus.RECEIVED.value, customer=self.customer)
        OrderFactory(status=OrderStatus.RECEIVED.value, customer=self.customer)
        OrderFactory(status=OrderStatus.DELIVERED.value, customer=self.customer)

        response = self.get(self.path, as_user=self.customer)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
        order_1 = response.data[0]
        self.assertEqual(len(order_1), 4)
        self.assertIn('pk', order_1)
        self.assertIn('status', order_1)
        self.assertIn('created_at', order_1)
        self.assertIn('order_items', order_1)

    def test_get_order_list_by_parameter(self):
        """GET /api/v1/orders/?status={string} returns a list of orders"""

        OrderFactory(status=OrderStatus.CANCELLED.value, customer=self.customer)

        response = self.get(self.path + f'?status={OrderStatus.RECEIVED.value}', as_user=self.customer)
        self.assertEqual(len(response.data), 0)

        response = self.get(self.path + f'?status={OrderStatus.CANCELLED.value}', as_user=self.customer)
        self.assertEqual(len(response.data), 1)

    def test_get_list_own_orders_only(self):
        """Asserts if the user can only access it's own orders"""

        other_user = CustomerFactory()
        OrderFactory(status=OrderStatus.CANCELLED.value, customer=self.customer)

        response = self.get(self.path, as_user=other_user)
        self.assertEqual(len(response.data), 0)


class OrderCreateTests(EndpointTestCase):

    def setUp(self):
        self.customer = CustomerFactory()
        self.restaurant = RestaurantFactory()
        self.path = reverse('api:order-create')

    def _get_payload(self):
        food_1 = FoodFactory()
        food_2 = FoodFactory()
        order_items = [
            {'food': food_1.pk, 'quantity': 85, 'amount': '0.02'},
            {'food': food_1.pk, 'quantity': 23, 'amount': '3.02'},
        ]

        return {
            'address': self.customer.address,
            'restaurant': self.restaurant.pk,
            'order_items': order_items
        }

    @patch('gelivery.api.endpoints.OrderCreateEndpoint._publish_message')
    def test_create_new_order(self, publish_func):
        """POST /api/v1/create-order creates an order and returns nothing"""
        publish_func.return_value = True

        payload = self._get_payload()

        response = self.post(self.path, payload, as_user=self.customer)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.customer.order_set.count(), 1)

        first_order = self.customer.order_set.first()
        self.assertEqual(first_order.status, OrderStatus.RECEIVED.value)

    def test_missing_required_attributes(self):
        """Asserts the all required keys must be in payload"""
        payload = self._get_payload()

        for key in ('address', 'restaurant', 'order_items'):
            tmp_val = payload[key]
            payload[key] = None
            response = self.post(self.path, payload, as_user=self.customer)
            self.assertEqual(response.status_code, 400)
            payload[key] = tmp_val


class OrderCompleteTests(EndpointTestCase):

    def setUp(self):
        self.customer = CustomerFactory()
        self.restaurant = RestaurantFactory()
        self.path = reverse('api:order-complete')

    def test_complete_order_successfully(self):
        """POST /api/v1/order-complete/ completes the given order id"""

        order_received = OrderFactory(status=OrderStatus.RECEIVED.value)
        payload = {
            'order_id': order_received.pk
        }
        response = self.post(self.path, payload)
        self.assertEqual(response.status_code, 201)
        order_received.refresh_from_db()
        self.assertEqual(order_received.status, OrderStatus.DELIVERED.value)

    def test_if_order_already_completed(self):
        """Asserts completed orders can't be updated"""
        order_completed = OrderFactory(status=OrderStatus.DELIVERED.value)
        payload = {
            'order_id': order_completed.pk
        }
        response = self.post(self.path, payload)
        self.assertEqual(response.status_code, 400)

    def test_if_order_not_exists(self):
        """Asserts 404 status is returned for not exist orders"""
        order_id = uuid.uuid4()
        payload = {
            'order_id': order_id
        }
        response = self.post(self.path, payload)
        self.assertEqual(response.status_code, 404)
