from django.db import models


class Offer(models.Model):
    title = models.CharField(max_length=150)
    discount = models.CharField(max_length=100) # e.g. "Flat 20% OFF", "15% OFF", "Free Dessert"
    min_spend = models.CharField(max_length=150) # e.g. "On all orders above ₹499"
    code = models.CharField(max_length=50, unique=True)
    tag = models.CharField(max_length=50, default='HOT DEAL')
    badge_color = models.CharField(max_length=100, default='bg-[#f47b20] text-white')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.discount}"
