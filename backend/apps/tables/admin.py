from django.contrib import admin
from django.utils.html import format_html
from .models import RestaurantTable


@admin.register(RestaurantTable)
class RestaurantTableAdmin(admin.ModelAdmin):
    list_display = ('table_display', 'seats', 'status_badge', 'floor_zone', 'updated_at')
    list_filter = ('status', 'floor_zone', 'seats')
    list_editable = ('floor_zone',)
    search_fields = ('table_number', 'floor_zone')
    ordering = ('table_number',)

    @admin.display(description='Table Number')
    def table_display(self, obj):
        return f"Table {obj.table_number}"

    @admin.display(description='Status')
    def status_badge(self, obj):
        colors = {
            'Available': ('#dcfce7', '#166534'),
            'Booked': ('#ffedd5', '#c2410c'),
            'Occupied': ('#fee2e2', '#991b1b'),
        }
        bg, fg = colors.get(obj.status, ('#f3f4f6', '#374151'))
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;">{}</span>',
            bg, fg, obj.status
        )
