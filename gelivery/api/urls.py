from django.urls import include, path

from .endpoints import (OrderCompleteEndpoint, OrderCreateEndpoint,
                        OrderListEndpoint)

app_name = 'api'

urlpatterns = [
    path('v1/', include([
        path('orders/', OrderListEndpoint.as_view(), name='order-list'),
        path('order-create/', OrderCreateEndpoint.as_view(), name='order-create'),
        path('order-complete/', OrderCompleteEndpoint.as_view(), name='order-complete')
    ]))
]
