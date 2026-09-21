from rest_framework import serializers
from .models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name',
            'tagline',
            'description',
            'hero_image',
            'outlet_name',
            'address',
            'phone',
            'email',
            'opening_hours',
            'gst_rate',
            'auto_accept',
            'is_active',
            'created_at',
            'updated_at',
        ]
