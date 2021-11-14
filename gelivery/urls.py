from django.conf.urls import include
from django.contrib import admin
from django.urls import path

app_name = 'gelivery'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('gelivery.api.urls')),
]
