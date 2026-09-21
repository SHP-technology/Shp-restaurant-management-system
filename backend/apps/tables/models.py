from django.db import models


class TableStatus(models.TextChoices):
    AVAILABLE = 'Available', 'Available'
    BOOKED = 'Booked', 'Booked'
    OCCUPIED = 'Occupied', 'Occupied'


class RestaurantTable(models.Model):
    table_number = models.PositiveIntegerField(unique=True)
    seats = models.PositiveIntegerField(default=4)
    status = models.CharField(
        max_length=20,
        choices=TableStatus.choices,
        default=TableStatus.AVAILABLE
    )
    floor_zone = models.CharField(max_length=100, default='Main Dining')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['table_number']

    @property
    def num(self):
        return self.table_number

    def __str__(self):
        return f"Table {self.table_number} ({self.status} - {self.seats} Seats)"
