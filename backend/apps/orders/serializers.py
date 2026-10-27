from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .models import Order, OrderItem, OrderType, OrderStatus, PaymentStatus, PaymentMethod
from apps.menu.models import MenuItem


class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_name = serializers.CharField(source='menu_item.name', read_only=True)
    menuItemId = serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all(),
        source='menu_item',
        write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menuItemId', 'menu_item_name', 'quantity', 'unit_price']
        read_only_fields = ['id', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    items_list = OrderItemSerializer(source='items', many=True, read_only=True)
    items = serializers.CharField(source='items_summary', read_only=True)
    customer = serializers.CharField(source='customer_display', read_only=True)
    price = serializers.CharField(source='price_display', read_only=True)
    type = serializers.CharField(source='order_type', required=False)
    phone = serializers.CharField(source='customer_phone', required=False)
    address = serializers.CharField(source='delivery_address', required=False)
    time = serializers.CharField(source='estimated_time', required=False)

    # Write-only fields for creation
    raw_items = serializers.ListField(child=serializers.DictField(), write_only=True, required=False)

    class Meta:
        model = Order
        fields = [
            'id',
            'type',
            'order_type',
            'customer',
            'customer_name',
            'customer_phone',
            'phone',
            'table_name',
            'items',
            'items_list',
            'raw_items',
            'price',
            'subtotal',
            'tax_amount',
            'delivery_fee',
            'discount_amount',
            'total_amount',
            'payment_status',
            'payment_method',
            'razorpay_order_id',
            'razorpay_payment_id',
            'razorpay_signature',
            'status',
            'address',
            'delivery_address',
            'delivery_instructions',
            'driver',
            'time',
            'estimated_time',
            'created_at',
            'updated_at',
        ]
        # Payment state and computed money fields are set only server-side, never by the client.
        read_only_fields = [
            'id',
            'payment_status',
            'razorpay_order_id',
            'razorpay_payment_id',
            'razorpay_signature',
            'status',
            'subtotal',
            'tax_amount',
            'total_amount',
            'created_at',
            'updated_at',
        ]

    @transaction.atomic
    def create(self, validated_data):
        raw_items = validated_data.pop('raw_items', [])
        order_type = validated_data.get('order_type', OrderType.DINE_IN)
        if 'type' in self.initial_data:
            order_type = self.initial_data['type']
            validated_data['order_type'] = order_type

        if not raw_items:
            raise serializers.ValidationError({'raw_items': 'An order must contain at least one item.'})

        order = Order.objects.create(**validated_data)

        subtotal = Decimal('0.00')
        for item_data in raw_items:
            item_id = item_data.get('menuItemId') or item_data.get('id') or item_data.get('menu_item')
            qty = int(item_data.get('quantity', item_data.get('count', 1)))
            if qty <= 0:
                raise serializers.ValidationError({'raw_items': f'Invalid quantity for item {item_id}.'})
            try:
                menu_item = MenuItem.objects.get(id=item_id)
            except MenuItem.DoesNotExist:
                # Roll back the whole order rather than silently undercharging.
                raise serializers.ValidationError({'raw_items': f'Menu item {item_id} does not exist.'})
            unit_price = Decimal(str(menu_item.price))
            OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=qty,
                unit_price=unit_price,
            )
            subtotal += (unit_price * qty)

        order.subtotal = subtotal
        order.tax_amount = round(subtotal * Decimal('0.05'), 2)  # 5% GST
        delivery_fee = Decimal(str(order.delivery_fee or '0.00'))
        discount_amount = Decimal(str(order.discount_amount or '0.00'))
        order.total_amount = order.subtotal + order.tax_amount + delivery_fee - discount_amount
        order.save()

        return order
