import uuid
from django.db import models


class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, default='SHP Restaurant')
    tagline = models.CharField(max_length=255, default='Good Food Great Moments')
    description = models.TextField(
        default='Delicious food, your way — dine in, delivery or celebration, we’ve got you covered.'
    )
    hero_image = models.URLField(
        default='https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1000&q=80'
    )
    outlet_name = models.CharField(max_length=255, default='SHP Restaurant - Civil Lines')
    address = models.TextField(default='Plot 14, Main Boulevard, Civil Lines, City')
    phone = models.CharField(max_length=50, default='+91 98765 43210 / 011 2345 6789')
    email = models.EmailField(default='contact@shprestaurant.com')
    opening_hours = models.CharField(max_length=150, default='Mon - Sun: 11:00 AM – 11:30 PM')
    gst_rate = models.CharField(max_length=20, default='5%')
    auto_accept = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.outlet_name}"
