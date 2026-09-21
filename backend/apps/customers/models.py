import random
from django.db import models


class Customer(models.Model):
    id = models.CharField(primary_key=True, max_length=50, default='')
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=30)
    email = models.EmailField(blank=True, default='')
    tag = models.CharField(max_length=50, default='New')  # 'VIP' | 'Regular' | 'New'
    visits = models.PositiveIntegerField(default=1)
    total_spent_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-visits']

    def save(self, *args, **kwargs):
        if not self.id:
            num = random.randint(1, 99)
            self.id = f"CUST-{num:02d}"
        super().save(*args, **kwargs)

    @property
    def totalSpent(self):
        return f"₹{int(self.total_spent_amount):,}"

    def __str__(self):
        return f"{self.name} ({self.phone}) - {self.tag}"
