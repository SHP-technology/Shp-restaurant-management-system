from django.contrib import admin
from django.utils.html import format_html
from .models import Restaurant


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'outlet_name', 'phone', 'email', 'gst_rate', 'auto_accept', 'is_active', 'created_at')
    list_filter = ('is_active', 'auto_accept', 'created_at')
    search_fields = ('name', 'outlet_name', 'phone', 'email', 'address')
    readonly_fields = ('id', 'created_at', 'updated_at')

    fieldsets = (
        ('Restaurant Profile', {
            'fields': ('id', 'name', 'tagline', 'description', 'hero_image')
        }),
        ('Outlet & Location', {
            'fields': ('outlet_name', 'address', 'phone', 'email', 'opening_hours')
        }),
        ('Operations & Billing', {
            'fields': ('gst_rate', 'auto_accept', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
