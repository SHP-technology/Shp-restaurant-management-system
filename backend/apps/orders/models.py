import uuid
import random
from decimal import Decimal
from django.db import models
from apps.restaurants.models import Restaurant
from apps.tables.models import RestaurantTable
from apps.menu.models import MenuItem


class OrderType(models.TextChoices):
    DINE_IN = 'Dine In', 'Dine In'
    DELIVERY = 'Delivery', 'Delivery'
    TAKEAWAY = 'Takeaway', 'Takeaway'


class OrderStatus(models.TextChoices):
    NEW = 'New', 'New'
    PREPARING = 'Preparing', 'Preparing'
    READY = 'Ready', 'Ready'
    OUT_FOR_DELIVERY = 'Out for Delivery', 'Out for Delivery'
    DELIVERED = 'Delivered', 'Delivered'
    COMPLETED = 'Completed', 'Completed'
    CANCELLED = 'Cancelled', 'Cancelled'


class PaymentStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    PAID = 'Paid', 'Paid'
    FAILED = 'Failed', 'Failed'
    REFUNDED = 'Refunded', 'Refunded'


class PaymentMethod(models.TextChoices):
    RAZORPAY = 'Razorpay', 'Razorpay Online (UPI / Cards / Netbanking)'
    CASH = 'Cash', 'Cash on Delivery'
    CARD = 'Card', 'Card at Counter'


class Order(models.Model):
    id = models.CharField(primary_key=True, max_length=50, default='')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True, related_name='orders')
    customer_name = models.CharField(max_length=150, default='Walk-in Guest')
    customer_phone = models.CharField(max_length=30, blank=True, default='')
    table = models.ForeignKey(RestaurantTable, on_delete=models.SET_NULL, null=True, blank=True)
    table_name = models.CharField(max_length=100, blank=True, default='')

    order_type = models.CharField(max_length=30, choices=OrderType.choices, default=OrderType.DINE_IN)
    status = models.CharField(max_length=30, choices=OrderStatus.choices, default=OrderStatus.NEW)

    # Financials
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    # Payment Gateway (Razorpay)
    payment_status = models.CharField(max_length=30, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    payment_method = models.CharField(max_length=50, default='Razorpay')
    razorpay_order_id = models.CharField(max_length=100, blank=True, default='')
    razorpay_payment_id = models.CharField(max_length=100, blank=True, default='')
    razorpay_signature = models.CharField(max_length=255, blank=True, default='')

    # Delivery logistics
    delivery_address = models.TextField(blank=True, default='')
    delivery_instructions = models.CharField(max_length=255, blank=True, default='')
    driver = models.CharField(max_length=100, blank=True, default='')
    estimated_time = models.CharField(max_length=50, blank=True, default='30 mins left')

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.id:
            prefix = '#DEL-' if self.order_type == OrderType.DELIVERY else '#'
            # Retry to avoid primary-key collisions under concurrent creates.
            for _ in range(20):
                candidate = f"{prefix}{random.randint(100000, 999999)}"
                if not Order.objects.filter(pk=candidate).exists():
                    self.id = candidate
                    break
            else:
                self.id = f"{prefix}{uuid.uuid4().hex[:10].upper()}"
        if not self.table_name and self.table:
            self.table_name = f"Table {self.table.table_number}"
        super().save(*args, **kwargs)

    @property
    def items_summary(self):
        item_list = list(self.items.select_related('menu_item').all())
        if not item_list:
            return "No items"
        count = sum(item.quantity for item in item_list)
        names = ", ".join([item.menu_item.name for item in item_list[:2]])
        return f"{count} items • {names}"

    @property
    def price_display(self):
        return f"₹{int(self.total_amount)}"

    @property
    def customer_display(self):
        if self.table_name:
            return f"{self.table_name} ({self.customer_name})"
        if self.delivery_address:
            return f"{self.customer_name} ({self.delivery_address.split(',')[0]})"
        return self.customer_name

    def __str__(self):
        return f"{self.id} - {self.order_type} ({self.status} - Payment: {self.payment_status})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name} in {self.order.id}"
