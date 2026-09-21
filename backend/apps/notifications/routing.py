from django.urls import re_path
from .consumers import RestaurantConsumer

websocket_urlpatterns = [
    re_path(r'^ws/restaurant/(?P<restaurant_id>[\w-]+)/?$', RestaurantConsumer.as_asgi()),
    re_path(r'^ws/?$', RestaurantConsumer.as_asgi()),
]
