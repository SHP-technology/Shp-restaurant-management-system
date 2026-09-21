from django.contrib import admin
from django.utils.html import format_html
from .models import Category, MenuItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'items_count', 'is_active')
    list_editable = ('display_order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('display_order', 'name')

    @admin.display(description='Dishes')
    def items_count(self, obj):
        return obj.items.count()


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price_display', 'dietary_badge', 'stock_badge', 'rating', 'prep_time', 'is_special')
    list_filter = ('category', 'is_in_stock', 'is_veg', 'is_special', 'created_at')
    list_editable = ('is_special',)
    search_fields = ('name', 'description', 'category__name')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Dish Info', {
            'fields': ('category', 'name', 'description', 'image')
        }),
        ('Pricing & Prep', {
            'fields': ('price', 'prep_time', 'rating')
        }),
        ('Attributes', {
            'fields': ('is_veg', 'is_special', 'is_in_stock')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    @admin.display(description='Price')
    def price_display(self, obj):
        return f"₹{obj.price}"

    @admin.display(description='Type')
    def dietary_badge(self, obj):
        if obj.is_veg:
            return format_html('<span style="color: #15803d; font-weight: bold;">● VEG</span>')
        return format_html('<span style="color: #b91c1c; font-weight: bold;">▲ NON-VEG</span>')

    @admin.display(description='Stock')
    def stock_badge(self, obj):
        if obj.is_in_stock:
            return format_html('<span style="background-color: #dcfce7; color: #166534; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px;">In Stock</span>')
        return format_html('<span style="background-color: #fee2e2; color: #991b1b; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px;">Out of Stock</span>')
