from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('menu_item', 'quantity', 'unit_price')
    readonly_fields = ()


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_display', 'order_type_badge', 'status_badge', 'total_display', 'items_summary', 'created_at')
    list_filter = ('order_type', 'status', 'created_at')
    search_fields = ('id', 'customer_name', 'customer_phone', 'table_name', 'delivery_address')
    readonly_fields = ('id', 'created_at', 'updated_at')
    inlines = [OrderItemInline]

    fieldsets = (
        ('Order Identification', {
            'fields': ('id', 'restaurant', 'order_type', 'status')
        }),
        ('Customer & Table', {
            'fields': ('customer_name', 'customer_phone', 'table', 'table_name')
        }),
        ('Delivery Logistics', {
            'fields': ('delivery_address', 'delivery_instructions', 'driver', 'estimated_time'),
            'classes': ('collapse',)
        }),
        ('Financials', {
            'fields': ('subtotal', 'tax_amount', 'delivery_fee', 'discount_amount', 'total_amount')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Total')
    def total_display(self, obj):
        return f"₹{obj.total_amount}"

    @admin.display(description='Type')
    def order_type_badge(self, obj):
        colors = {
            'Dine In': ('#e0f2fe', '#0369a1'),
            'Delivery': ('#fef3c7', '#b45309'),
            'Takeaway': ('#f3e8ff', '#6b21a8'),
        }
        bg, fg = colors.get(obj.order_type, ('#f3f4f6', '#374151'))
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;">{}</span>',
            bg, fg, obj.order_type
        )

    @admin.display(description='Status')
    def status_badge(self, obj):
        colors = {
            'New': ('#dbeafe', '#1d4ed8'),
            'Preparing': ('#ffedd5', '#c2410c'),
            'Ready': ('#dcfce7', '#15803d'),
            'Out for Delivery': ('#fef9c3', '#a16207'),
            'Delivered': ('#d1fae5', '#047857'),
            'Completed': ('#f3f4f6', '#374151'),
            'Cancelled': ('#fee2e2', '#b91c1c'),
        }
        bg, fg = colors.get(obj.status, ('#f3f4f6', '#374151'))
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;">{}</span>',
            bg, fg, obj.status
        )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity', 'unit_price')
    list_filter = ('order__order_type', 'order__status')
    search_fields = ('order__id', 'menu_item__name')
