from django.contrib import admin
from django.utils.html import format_html
from .models import RestaurantTable, TableStatus


@admin.register(RestaurantTable)
class RestaurantTableAdmin(admin.ModelAdmin):
    list_display = (
        'table_display',
        'seats_display',
        'status_badge',
        'floor_zone_badge',
        'updated_at_display',
    )
    list_filter = ('status', 'floor_zone', 'seats')
    list_editable = ()
    search_fields = ('table_number', 'floor_zone')
    ordering = ('table_number',)
    save_on_top = True

    fieldsets = (
        ('Table Configuration', {
            'fields': ('table_number', 'seats', 'floor_zone', 'status'),
            'classes': ('extrapretty',),
        }),
    )

    actions = ['mark_available', 'mark_occupied', 'mark_booked']

    @admin.display(description='Table', ordering='table_number')
    def table_display(self, obj):
        return format_html(
            '<div style="font-weight: 700; color: #0f172a; font-size: 14px;">'
            '<i class="fas fa-chair text-primary me-2"></i> Table #{}'
            '</div>',
            obj.table_number
        )

    @admin.display(description='Capacity', ordering='seats')
    def seats_display(self, obj):
        return format_html(
            '<span style="background-color: #f1f5f9; color: #334155; padding: 3px 8px; border-radius: 6px; font-weight: 600; font-size: 12px;">'
            '<i class="fas fa-users text-muted me-1"></i> {} Seats</span>',
            obj.seats
        )

    @admin.display(description='Live Status', ordering='status')
    def status_badge(self, obj):
        configs = {
            TableStatus.AVAILABLE: ('#dcfce7', '#15803d', 'fas fa-check-circle', 'Available'),
            TableStatus.BOOKED: ('#ffedd5', '#c2410c', 'fas fa-calendar-check', 'Booked / Reserved'),
            TableStatus.OCCUPIED: ('#fee2e2', '#b91c1c', 'fas fa-utensils', 'Occupied / Dining'),
        }
        bg, fg, icon, label = configs.get(obj.status, ('#f3f4f6', '#374151', 'fas fa-info-circle', obj.status))
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 4px 10px; border-radius: 9999px; font-weight: 600; font-size: 11px; display: inline-flex; align-items: center; gap: 5px;">'
            '<i class="{}"></i> {}</span>',
            bg, fg, icon, label
        )

    @admin.display(description='Floor Zone', ordering='floor_zone')
    def floor_zone_badge(self, obj):
        return format_html(
            '<span style="background-color: #e0e7ff; color: #4338ca; padding: 2px 8px; border-radius: 6px; font-weight: 500; font-size: 12px;">'
            '<i class="fas fa-map-marker-alt me-1"></i> {}</span>',
            obj.floor_zone
        )

    @admin.display(description='Last Status Update', ordering='updated_at')
    def updated_at_display(self, obj):
        return obj.updated_at.strftime('%d %b %Y, %I:%M %p')

    # Bulk actions
    @admin.action(description='Mark selected tables as Available')
    def mark_available(self, request, queryset):
        count = queryset.update(status=TableStatus.AVAILABLE)
        self.message_user(request, f"{count} table(s) marked as Available.")

    @admin.action(description='Mark selected tables as Occupied')
    def mark_occupied(self, request, queryset):
        count = queryset.update(status=TableStatus.OCCUPIED)
        self.message_user(request, f"{count} table(s) marked as Occupied.")

    @admin.action(description='Mark selected tables as Booked')
    def mark_booked(self, request, queryset):
        count = queryset.update(status=TableStatus.BOOKED)
        self.message_user(request, f"{count} table(s) marked as Booked.")
