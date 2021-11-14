import json

import redis
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse


class OrderConsumer:

    def __init__(self, redis_host, redis_port=None):
        redis_port = redis_port or 6379
        self.instance = redis.StrictRedis(host=redis_host, port=redis_port)

    def order_run(self):
        pubsub = self.instance.pubsub(ignore_subscribe_messages=True)
        pubsub.subscribe('orders')
        for entry in pubsub.listen():
            data = json.loads(entry['data'])
            if data['message'] == 'order_created':
                self.callback(data['order_id'])

    def callback(self, order_id):
        payload = json.dumps({'order_id': order_id})
        headers = {'Content-Type': 'application/json'}
        endpoint = reverse('api:order-complete')
        requests.post(f'http://app:8000{endpoint}', data=payload, headers=headers)


class Command(BaseCommand):

    def handle(self, *args, **options):
        OrderConsumer(settings.REDIS_HOSTNAME).order_run()
