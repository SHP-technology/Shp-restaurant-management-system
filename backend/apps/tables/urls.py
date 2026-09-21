from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TableViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'', TableViewSet, basename='table')

urlpatterns = [
    path('', include(router.urls)),
]
