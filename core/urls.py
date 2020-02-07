# -*- coding: utf-8 -*-
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.views import HealthCheckViewSet

routers = DefaultRouter()
routers.register('', HealthCheckViewSet, base_name='core')

urlpatterns = [
    path('', include(routers.get_urls()))
]
