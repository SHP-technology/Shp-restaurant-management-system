import random
from django.db import models
from apps.tables.models import RestaurantTable


class TableReservation(models.Model):
    id = models.CharField(primary_key=True, max_length=50, default='')
    name = models.CharField(max_length=150, default='Guest')
    phone = models.CharField(max_length=30, default='+91 98765 43210')
    date = models.CharField(max_length=50, default='2026-09-10')
    time = models.CharField(max_length=50, default='7:30 PM')
    guests = models.CharField(max_length=50, default='2 People')
    area = models.CharField(max_length=100, default='Main Dining')
    special_request = models.TextField(blank=True, default='')
    status = models.CharField(max_length=30, default='Confirmed')
    assigned_table = models.ForeignKey(RestaurantTable, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.id:
            num = random.randint(100, 999)
            self.id = f"RES-{num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.name} ({self.date} {self.time})"


class PartyBooking(models.Model):
    id = models.CharField(primary_key=True, max_length=50, default='')
    occasion = models.CharField(max_length=150, default='Birthday Bash')
    client = models.CharField(max_length=150, default='Client')
    phone = models.CharField(max_length=30, default='')
    date = models.CharField(max_length=50, default='2026-10-15')
    guests = models.CharField(max_length=50, default='25-50 Guests')
    requirements = models.TextField(blank=True, default='Decoration, Cake, Music')
    status = models.CharField(max_length=50, default='Confirmed')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.id:
            num = random.randint(500, 999)
            self.id = f"PRT-{num}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.id} - {self.occasion} ({self.client})"
