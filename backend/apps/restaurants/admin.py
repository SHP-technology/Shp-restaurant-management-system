from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Restaurant


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        'hero_thumbnail',
        'name',
        'outlet_name',
        'contact_info',
        'gst_rate',
        'auto_accept_badge',
        'is_active_badge',
        'created_at_display',
    )
    list_display_links = ('hero_thumbnail', 'name')
    list_filter = ('is_active', 'auto_accept', 'created_at')
    list_editable = ()
    search_fields = ('name', 'outlet_name', 'phone', 'email', 'address')
    readonly_fields = ('id', 'hero_preview_large', 'created_at', 'updated_at')
    save_on_top = True

    fieldsets = (
        ('Restaurant Brand & Identity', {
            'fields': ('id', 'name', 'tagline', 'description', 'hero_image', 'hero_preview_large'),
            'classes': ('extrapretty',),
        }),
        ('Outlet Location & Contact Details', {
            'fields': ('outlet_name', 'address', 'phone', 'email', 'opening_hours'),
            'classes': ('extrapretty',),
        }),
        ('Operations & Automated Settings', {
            'fields': ('gst_rate', 'auto_accept', 'is_active'),
            'classes': ('extrapretty',),
        }),
        ('System Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    actions = ['enable_auto_accept', 'disable_auto_accept', 'activate_outlet', 'deactivate_outlet']

    @admin.display(description='Preview')
    def hero_thumbnail(self, obj):
        if obj.hero_image:
            return format_html(
                '<img src="{}" style="width: 52px; height: 38px; object-fit: cover; border-radius: 6px; border: 1px solid #e2e8f0; box-shadow: 0 1px 2px rgba(0,0,0,0.05);" />',
                obj.hero_image
            )
        return mark_safe(
            '<div style="width: 52px; height: 38px; background-color: #f1f5f9; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: #94a3b8;"><i class="fas fa-store"></i></div>'
        )

    @admin.display(description='Large Preview')
    def hero_preview_large(self, obj):
        if obj.hero_image:
            return format_html(
                '<div style="margin-top: 6px;"><img src="{}" style="max-height: 180px; border-radius: 8px; border: 1px solid #cbd5e1; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);" /></div>',
                obj.hero_image
            )
        return mark_safe('<span style="color: #94a3b8;">No hero image uploaded</span>')

    @admin.display(description='Contact')
    def contact_info(self, obj):
        return format_html(
            '<div style="font-size: 12px; line-height: 1.4;">'
            '<div><i class="fas fa-phone-alt text-muted me-1"></i> {}</div>'
            '<div class="text-muted"><i class="fas fa-envelope text-muted me-1"></i> {}</div>'
            '</div>',
            obj.phone,
            obj.email
        )

    @admin.display(description='Auto Accept Orders')
    def auto_accept_badge(self, obj):
        if obj.auto_accept:
            return mark_safe(
                '<span style="background-color: #e0f2fe; color: #0369a1; padding: 3px 8px; border-radius: 9999px; font-weight: 600; font-size: 11px;">'
                '<i class="fas fa-bolt me-1"></i> Enabled</span>'
            )
        return mark_safe(
            '<span style="background-color: #f1f5f9; color: #64748b; padding: 3px 8px; border-radius: 9999px; font-weight: 600; font-size: 11px;">'
            '<i class="fas fa-pause-circle me-1"></i> Manual</span>'
        )

    @admin.display(description='Status')
    def is_active_badge(self, obj):
        if obj.is_active:
            return mark_safe(
                '<span style="background-color: #dcfce7; color: #15803d; padding: 3px 8px; border-radius: 9999px; font-weight: 600; font-size: 11px;">'
                '<i class="fas fa-check-circle me-1"></i> Active</span>'
            )
        return mark_safe(
            '<span style="background-color: #fee2e2; color: #b91c1c; padding: 3px 8px; border-radius: 9999px; font-weight: 600; font-size: 11px;">'
            '<i class="fas fa-times-circle me-1"></i> Inactive</span>'
        )

    @admin.display(description='Created On', ordering='created_at')
    def created_at_display(self, obj):
        return obj.created_at.strftime('%d %b %Y')

    # Bulk actions
    @admin.action(description='Enable Auto-Accept for selected outlets')
    def enable_auto_accept(self, request, queryset):
        count = queryset.update(auto_accept=True)
        self.message_user(request, f"Auto-accept enabled for {count} outlet(s).")

    @admin.action(description='Disable Auto-Accept for selected outlets')
    def disable_auto_accept(self, request, queryset):
        count = queryset.update(auto_accept=False)
        self.message_user(request, f"Auto-accept disabled for {count} outlet(s).")

    @admin.action(description='Activate selected outlets')
    def activate_outlet(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"{count} outlet(s) activated.")

    @admin.action(description='Deactivate selected outlets')
    def deactivate_outlet(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"{count} outlet(s) deactivated.")
