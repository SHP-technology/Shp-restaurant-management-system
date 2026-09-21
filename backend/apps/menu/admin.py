from django.contrib import admin
from django.utils.html import format_html
from .models import Category, MenuItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('image_thumbnail', 'name', 'display_order', 'items_count_badge', 'is_active_badge')
    list_display_links = ('image_thumbnail', 'name')
    list_editable = ('display_order',)
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('display_order', 'name')
    save_on_top = True

    fieldsets = (
        ('Category Details', {
            'fields': ('name', 'image', 'display_order', 'is_active'),
            'classes': ('extrapretty',),
        }),
    )

    actions = ['activate_categories', 'deactivate_categories']

    @admin.display(description='Icon / Image')
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 40px; height: 40px; object-fit: cover; border-radius: 8px; border: 1px solid #e2e8f0;" />',
                obj.image
            )
        return format_html(
            '<div style="width: 40px; height: 40px; background-color: #f1f5f9; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #94a3b8;"><i class="fas fa-layer-group"></i></div>'
        )

    @admin.display(description='Total Dishes')
    def items_count_badge(self, obj):
        count = obj.items.count()
        return format_html(
            '<span style="background-color: #e0f2fe; color: #0284c7; padding: 2px 8px; border-radius: 9999px; font-weight: 700; font-size: 12px;">'
            '<i class="fas fa-utensils me-1"></i> {}</span>',
            count
        )

    @admin.display(description='Status')
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background-color: #dcfce7; color: #15803d; padding: 3px 8px; border-radius: 9999px; font-weight: 600; font-size: 11px;">'
                '<i class="fas fa-check-circle me-1"></i> Active</span>'
            )
        return format_html(
            '<span style="background-color: #fee2e2; color: #b91c1c; padding: 3px 8px; border-radius: 9999px; font-weight: 600; font-size: 11px;">'
            '<i class="fas fa-times-circle me-1"></i> Inactive</span>'
        )

    @admin.action(description='Activate selected categories')
    def activate_categories(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"{count} category/categories activated.")

    @admin.action(description='Deactivate selected categories')
    def deactivate_categories(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"{count} category/categories deactivated.")


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = (
        'dish_thumbnail',
        'name',
        'category_badge',
        'price_display',
        'dietary_badge',
        'stock_badge',
        'rating_badge',
        'prep_time_display',
        'is_special_badge',
    )
    list_display_links = ('dish_thumbnail', 'name')
    list_filter = ('category', 'is_in_stock', 'is_veg', 'is_special', 'created_at')
    list_editable = ()
    search_fields = ('name', 'description', 'category__name')
    readonly_fields = ('dish_preview_large', 'created_at', 'updated_at')
    save_on_top = True

    fieldsets = (
        ('Dish Identification & Media', {
            'fields': ('name', 'category', 'description', 'image', 'dish_preview_large'),
            'classes': ('extrapretty',),
        }),
        ('Pricing & Kitchen Operations', {
            'fields': ('price', 'prep_time', 'rating'),
            'classes': ('extrapretty',),
        }),
        ('Inventory & Highlights', {
            'fields': ('is_veg', 'is_special', 'is_in_stock'),
            'classes': ('extrapretty',),
        }),
        ('System Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    actions = [
        'mark_in_stock',
        'mark_out_of_stock',
        'mark_as_special',
        'remove_from_special',
        'mark_as_veg',
        'mark_as_non_veg',
    ]

    @admin.display(description='Dish Image')
    def dish_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 44px; height: 44px; object-fit: cover; border-radius: 8px; border: 1px solid #e2e8f0; box-shadow: 0 1px 2px rgba(0,0,0,0.06);" />',
                obj.image
            )
        return format_html(
            '<div style="width: 44px; height: 44px; background-color: #f1f5f9; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #94a3b8;"><i class="fas fa-utensils"></i></div>'
        )

    @admin.display(description='Image Preview')
    def dish_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<div style="margin-top: 6px;"><img src="{}" style="max-height: 200px; border-radius: 8px; border: 1px solid #cbd5e1; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);" /></div>',
                obj.image
            )
        return format_html('<span style="color: #94a3b8;">No dish image provided</span>')

    @admin.display(description='Category', ordering='category__name')
    def category_badge(self, obj):
        return format_html(
            '<span style="background-color: #f3f4f6; color: #374151; padding: 3px 8px; border-radius: 6px; font-weight: 500; font-size: 12px;">'
            '<i class="fas fa-tag text-muted me-1"></i> {}</span>',
            obj.category.name
        )

    @admin.display(description='Price', ordering='price')
    def price_display(self, obj):
        return format_html('<span style="font-weight: 700; color: #0f172a; font-size: 13px;">₹{}</span>', obj.price)

    @admin.display(description='Food Type', ordering='is_veg')
    def dietary_badge(self, obj):
        if obj.is_veg:
            return format_html(
                '<span style="display: inline-flex; align-items: center; gap: 4px; border: 1.5px solid #16a34a; padding: 2px 6px; border-radius: 4px; font-weight: 700; font-size: 11px; color: #16a34a; background-color: #f0fdf4;">'
                '<span style="display: inline-block; width: 7px; height: 7px; background-color: #16a34a; border-radius: 50%;"></span> VEG</span>'
            )
        return format_html(
            '<span style="display: inline-flex; align-items: center; gap: 4px; border: 1.5px solid #dc2626; padding: 2px 6px; border-radius: 4px; font-weight: 700; font-size: 11px; color: #dc2626; background-color: #fef2f2;">'
            '<span style="display: inline-block; width: 0; height: 0; border-left: 4px solid transparent; border-right: 4px solid transparent; border-bottom: 7px solid #dc2626;"></span> NON-VEG</span>'
        )

    @admin.display(description='Stock Status', ordering='is_in_stock')
    def stock_badge(self, obj):
        if obj.is_in_stock:
            return format_html(
                '<span style="background-color: #dcfce7; color: #15803d; padding: 3px 8px; border-radius: 9999px; font-weight: 600; font-size: 11px;">'
                '<i class="fas fa-check-circle me-1"></i> In Stock</span>'
            )
        return format_html(
            '<span style="background-color: #fee2e2; color: #b91c1c; padding: 3px 8px; border-radius: 9999px; font-weight: 600; font-size: 11px;">'
            '<i class="fas fa-ban me-1"></i> Out of Stock</span>'
        )

    @admin.display(description='Rating', ordering='rating')
    def rating_badge(self, obj):
        return format_html(
            '<span style="background-color: #fef3c7; color: #b45309; padding: 2px 6px; border-radius: 6px; font-weight: 700; font-size: 11px;">'
            '<i class="fas fa-star text-warning me-1"></i> {}</span>',
            obj.rating
        )

    @admin.display(description='Prep Time')
    def prep_time_display(self, obj):
        return format_html(
            '<span style="color: #64748b; font-size: 12px;"><i class="far fa-clock me-1"></i> {}</span>',
            obj.prep_time
        )

    @admin.display(description="Chef's Special", ordering='is_special')
    def is_special_badge(self, obj):
        if obj.is_special:
            return format_html(
                '<span style="background-color: #fdf2f8; color: #db2777; border: 1px solid #fbcfe8; padding: 2px 8px; border-radius: 9999px; font-weight: 600; font-size: 11px;">'
                '<i class="fas fa-award me-1"></i> Special</span>'
            )
        return format_html('<span style="color: #cbd5e1;">-</span>')

    # Bulk actions
    @admin.action(description='Mark selected dishes as In Stock')
    def mark_in_stock(self, request, queryset):
        count = queryset.update(is_in_stock=True)
        self.message_user(request, f"{count} dish(es) marked as In Stock.")

    @admin.action(description='Mark selected dishes as Out of Stock')
    def mark_out_of_stock(self, request, queryset):
        count = queryset.update(is_in_stock=False)
        self.message_user(request, f"{count} dish(es) marked as Out of Stock.")

    @admin.action(description="Mark selected dishes as Chef's Special")
    def mark_as_special(self, request, queryset):
        count = queryset.update(is_special=True)
        self.message_user(request, f"{count} dish(es) marked as Chef's Special.")

    @admin.action(description="Remove selected dishes from Chef's Special")
    def remove_from_special(self, request, queryset):
        count = queryset.update(is_special=False)
        self.message_user(request, f"{count} dish(es) removed from Chef's Special.")

    @admin.action(description='Mark selected dishes as Vegetarian (VEG)')
    def mark_as_veg(self, request, queryset):
        count = queryset.update(is_veg=True)
        self.message_user(request, f"{count} dish(es) marked as Vegetarian.")

    @admin.action(description='Mark selected dishes as Non-Vegetarian (NON-VEG)')
    def mark_as_non_veg(self, request, queryset):
        count = queryset.update(is_veg=False)
        self.message_user(request, f"{count} dish(es) marked as Non-Vegetarian.")
