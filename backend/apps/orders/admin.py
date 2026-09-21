from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem, OrderStatus, OrderType


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('menu_item', 'quantity', 'unit_price', 'line_total_display')
    readonly_fields = ('line_total_display',)
    show_change_link = True

    @admin.display(description='Line Total')
    def line_total_display(self, obj):
        if obj.unit_price and obj.quantity:
            total = obj.unit_price * obj.quantity
            return format_html('<span style="font-weight: 700; color: #0f172a;">₹{}</span>', total)
        return '₹0.00'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_id_badge',
        'customer_display_info',
        'order_type_badge',
        'location_info',
        'status_badge',
        'items_count_badge',
        'total_amount_display',
        'created_at_display',
    )
    list_display_links = ('order_id_badge', 'customer_display_info')
    list_filter = ('order_type', 'status', 'created_at', 'restaurant')
    date_hierarchy = 'created_at'
    search_fields = ('id', 'customer_name', 'customer_phone', 'table_name', 'delivery_address', 'driver')
    readonly_fields = ('id', 'created_at', 'updated_at', 'order_summary_card')
    inlines = [OrderItemInline]
    save_on_top = True

    fieldsets = (
        ('Order Overview', {
            'fields': ('id', 'restaurant', 'order_type', 'status', 'order_summary_card'),
            'classes': ('extrapretty',),
        }),
        ('Customer & Table Assignment', {
            'fields': ('customer_name', 'customer_phone', 'table', 'table_name'),
            'classes': ('extrapretty',),
        }),
        ('Delivery & Dispatch Details', {
            'fields': ('delivery_address', 'delivery_instructions', 'driver', 'estimated_time'),
            'classes': ('extrapretty',),
        }),
        ('Billing & Financial Breakdown', {
            'fields': ('subtotal', 'tax_amount', 'delivery_fee', 'discount_amount', 'total_amount'),
            'classes': ('extrapretty',),
        }),
        ('Audit Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    actions = [
        'mark_preparing',
        'mark_ready',
        'mark_out_for_delivery',
        'mark_delivered',
        'mark_completed',
        'mark_cancelled',
    ]

    @admin.display(description='Order ID', ordering='id')
    def order_id_badge(self, obj):
        if obj.order_type == OrderType.DELIVERY:
            return format_html(
                '<span style="background-color: #fef3c7; color: #92400e; border: 1px solid #fde68a; padding: 3px 8px; border-radius: 6px; font-weight: 700; font-family: monospace; font-size: 12px;">'
                '<i class="fas fa-motorcycle me-1"></i> {}</span>',
                obj.id
            )
        return format_html(
            '<span style="background-color: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; padding: 3px 8px; border-radius: 6px; font-weight: 700; font-family: monospace; font-size: 12px;">'
            '<i class="fas fa-receipt me-1"></i> {}</span>',
            obj.id
        )

    @admin.display(description='Customer')
    def customer_display_info(self, obj):
        phone_html = f'<div class="text-muted" style="font-size: 11px;"><i class="fas fa-phone-alt me-1"></i> {obj.customer_phone}</div>' if obj.customer_phone else ''
        return format_html(
            '<div>'
            '<div style="font-weight: 600; color: #1e293b;">{}</div>'
            '{}'
            '</div>',
            obj.customer_name,
            format_html(phone_html)
        )

    @admin.display(description='Type', ordering='order_type')
    def order_type_badge(self, obj):
        configs = {
            OrderType.DINE_IN: ('#e0f2fe', '#0369a1', 'fas fa-utensils'),
            OrderType.DELIVERY: ('#fef3c7', '#b45309', 'fas fa-truck'),
            OrderType.TAKEAWAY: ('#f3e8ff', '#6b21a8', 'fas fa-shopping-bag'),
        }
        bg, fg, icon = configs.get(obj.order_type, ('#f3f4f6', '#374151', 'fas fa-tag'))
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 8px; border-radius: 9999px; font-weight: 600; font-size: 11px;">'
            '<i class="{} me-1"></i> {}</span>',
            bg, fg, icon, obj.order_type
        )

    @admin.display(description='Location / Table')
    def location_info(self, obj):
        if obj.order_type == OrderType.DINE_IN:
            table_str = obj.table_name or (f"Table #{obj.table.table_number}" if obj.table else 'Unassigned')
            return format_html('<span style="font-weight: 600; color: #334155;"><i class="fas fa-chair text-primary me-1"></i> {}</span>', table_str)
        elif obj.order_type == OrderType.DELIVERY:
            addr = obj.delivery_address[:30] + '...' if len(obj.delivery_address) > 30 else (obj.delivery_address or 'Pending address')
            return format_html('<span style="font-size: 12px; color: #64748b;" title="{}"><i class="fas fa-map-marker-alt text-danger me-1"></i> {}</span>', obj.delivery_address, addr)
        return format_html('<span style="color: #64748b;"><i class="fas fa-store me-1"></i> Pickup Counter</span>')

    @admin.display(description='Status', ordering='status')
    def status_badge(self, obj):
        configs = {
            OrderStatus.NEW: ('#dbeafe', '#1d4ed8', 'fas fa-sparkles'),
            OrderStatus.PREPARING: ('#ffedd5', '#c2410c', 'fas fa-fire'),
            OrderStatus.READY: ('#dcfce7', '#15803d', 'fas fa-bell'),
            OrderStatus.OUT_FOR_DELIVERY: ('#fef9c3', '#a16207', 'fas fa-biking'),
            OrderStatus.DELIVERED: ('#d1fae5', '#047857', 'fas fa-check-double'),
            OrderStatus.COMPLETED: ('#f1f5f9', '#475569', 'fas fa-flag-checkered'),
            OrderStatus.CANCELLED: ('#fee2e2', '#b91c1c', 'fas fa-ban'),
        }
        bg, fg, icon = configs.get(obj.status, ('#f3f4f6', '#374151', 'fas fa-circle'))
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 4px 10px; border-radius: 9999px; font-weight: 700; font-size: 11px; display: inline-flex; align-items: center; gap: 4px;">'
            '<i class="{}"></i> {}</span>',
            bg, fg, icon, obj.status
        )

    @admin.display(description='Items')
    def items_count_badge(self, obj):
        items = list(obj.items.select_related('menu_item').all())
        total_items = sum(i.quantity for i in items)
        if not items:
            return format_html('<span style="color: #94a3b8; font-size: 11px;">0 items</span>')
        first_dish = items[0].menu_item.name
        suffix = f" +{len(items)-1} more" if len(items) > 1 else ""
        return format_html(
            '<span title="{} items total">'
            '<span style="background-color: #f1f5f9; color: #334155; padding: 2px 6px; border-radius: 6px; font-weight: 700; font-size: 11px; margin-right: 4px;">{}x</span>'
            '<span style="font-size: 12px; color: #475569;">{}{}</span>'
            '</span>',
            total_items, total_items, first_dish, suffix
        )

    @admin.display(description='Total Amount', ordering='total_amount')
    def total_amount_display(self, obj):
        return format_html('<span style="font-weight: 800; color: #0f172a; font-size: 13px;">₹{}</span>', obj.total_amount)

    @admin.display(description='Placed At', ordering='created_at')
    def created_at_display(self, obj):
        return obj.created_at.strftime('%d %b, %I:%M %p')

    @admin.display(description='Order Quick Summary')
    def order_summary_card(self, obj):
        if not obj.pk:
            return "Save order first to view summary"
        items_html = "".join([
            f"<li style='margin-bottom: 4px;'><b>{i.quantity}x</b> {i.menu_item.name} — ₹{i.unit_price * i.quantity}</li>"
            for i in obj.items.select_related('menu_item').all()
        ])
        return format_html(
            '<div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px 16px; max-width: 500px;">'
            '<div style="font-weight: 700; margin-bottom: 8px; color: #1e293b;">Order Items & Totals:</div>'
            '<ul style="padding-left: 20px; margin-bottom: 8px; color: #334155; font-size: 13px;">{}</ul>'
            '<div style="border-top: 1px dashed #cbd5e1; padding-top: 6px; font-weight: 700; color: #0f172a; font-size: 14px;">Total: ₹{}</div>'
            '</div>',
            format_html(items_html) if items_html else "<li>No items attached</li>",
            obj.total_amount
        )

    # Bulk workflow actions
    @admin.action(description='Mark as Preparing (Kitchen In-Progress)')
    def mark_preparing(self, request, queryset):
        count = queryset.update(status=OrderStatus.PREPARING)
        self.message_user(request, f"{count} order(s) updated to Preparing.")

    @admin.action(description='Mark as Ready (Kitchen Completed)')
    def mark_ready(self, request, queryset):
        count = queryset.update(status=OrderStatus.READY)
        self.message_user(request, f"{count} order(s) updated to Ready.")

    @admin.action(description='Mark as Out for Delivery')
    def mark_out_for_delivery(self, request, queryset):
        count = queryset.update(status=OrderStatus.OUT_FOR_DELIVERY)
        self.message_user(request, f"{count} order(s) updated to Out for Delivery.")

    @admin.action(description='Mark as Delivered')
    def mark_delivered(self, request, queryset):
        count = queryset.update(status=OrderStatus.DELIVERED)
        self.message_user(request, f"{count} order(s) updated to Delivered.")

    @admin.action(description='Mark as Completed')
    def mark_completed(self, request, queryset):
        count = queryset.update(status=OrderStatus.COMPLETED)
        self.message_user(request, f"{count} order(s) marked as Completed.")

    @admin.action(description='Mark as Cancelled')
    def mark_cancelled(self, request, queryset):
        count = queryset.update(status=OrderStatus.CANCELLED)
        self.message_user(request, f"{count} order(s) marked as Cancelled.")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item', 'quantity_badge', 'unit_price_display', 'line_total_display')
    list_filter = ('order__order_type', 'order__status', 'menu_item__category')
    search_fields = ('order__id', 'menu_item__name', 'order__customer_name')
    save_on_top = True

    @admin.display(description='Quantity', ordering='quantity')
    def quantity_badge(self, obj):
        return format_html(
            '<span style="background-color: #f1f5f9; color: #1e293b; font-weight: 700; padding: 2px 8px; border-radius: 6px;">{}x</span>',
            obj.quantity
        )

    @admin.display(description='Unit Price', ordering='unit_price')
    def unit_price_display(self, obj):
        return f"₹{obj.unit_price}"

    @admin.display(description='Line Total')
    def line_total_display(self, obj):
        return format_html('<span style="font-weight: 700; color: #0f172a;">₹{}</span>', obj.unit_price * obj.quantity)
