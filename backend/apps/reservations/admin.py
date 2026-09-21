from django.contrib import admin
from django.utils.html import format_html
from .models import TableReservation, PartyBooking


@admin.register(TableReservation)
class TableReservationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'date', 'time', 'guests', 'area', 'status_badge', 'created_at')
    list_filter = ('status', 'area', 'date', 'created_at')
    search_fields = ('id', 'name', 'phone', 'special_request')
    readonly_fields = ('id', 'created_at')

    @admin.display(description='Status')
    def status_badge(self, obj):
        colors = {
            'Confirmed': ('#dcfce7', '#166534'),
            'Pending': ('#fef3c7', '#b45309'),
            'Cancelled': ('#fee2e2', '#991b1b'),
        }
        bg, fg = colors.get(obj.status, ('#f3f4f6', '#374151'))
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;">{}</span>',
            bg, fg, obj.status
        )


@admin.register(PartyBooking)
class PartyBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'occasion', 'client', 'phone', 'date', 'guests', 'status_badge', 'created_at')
    list_filter = ('occasion', 'status', 'date', 'created_at')
    search_fields = ('id', 'client', 'phone', 'occasion', 'requirements')
    readonly_fields = ('id', 'created_at')

    @admin.display(description='Status')
    def status_badge(self, obj):
        colors = {
            'Confirmed': ('#dcfce7', '#166534'),
            'Pending Inquiry': ('#ffedd5', '#c2410c'),
            'Cancelled': ('#fee2e2', '#991b1b'),
        }
        bg, fg = colors.get(obj.status, ('#f3f4f6', '#374151'))
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;">{}</span>',
            bg, fg, obj.status
        )
