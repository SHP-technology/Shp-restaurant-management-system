from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Offer


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = (
        'coupon_code_badge',
        'title',
        'discount_badge',
        'min_spend_display',
        'tag_badge',
        'is_active_badge',
        'created_at_display',
    )
    list_display_links = ('coupon_code_badge', 'title')
    list_filter = ('is_active', 'created_at')
    list_editable = ()
    search_fields = ('code', 'title', 'discount', 'tag')
    readonly_fields = ('created_at',)
    save_on_top = True

    fieldsets = (
        ('Coupon & Discount Details', {
            'fields': ('code', 'title', 'discount', 'min_spend'),
            'classes': ('extrapretty',),
        }),
        ('Display & Promotional Tags', {
            'fields': ('tag', 'badge_color', 'is_active'),
            'classes': ('extrapretty',),
        }),
        ('Audit Information', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    actions = ['activate_offers', 'deactivate_offers']

    @admin.display(description='Promo Code', ordering='code')
    def coupon_code_badge(self, obj):
        return format_html(
            '<span style="background-color: #fff7ed; color: #c2410c; border: 1.5px dashed #fb923c; padding: 3px 10px; border-radius: 6px; font-weight: 800; font-family: monospace; font-size: 12px; letter-spacing: 0.5px;">'
            '<i class="fas fa-ticket-alt me-1"></i> {}</span>',
            obj.code
        )

    @admin.display(description='Discount Value')
    def discount_badge(self, obj):
        return format_html(
            '<span style="background-color: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; padding: 2px 8px; border-radius: 9999px; font-weight: 700; font-size: 11px;">'
            '<i class="fas fa-percent me-1"></i> {}</span>',
            obj.discount
        )

    @admin.display(description='Min Order Requirement')
    def min_spend_display(self, obj):
        return format_html('<span style="color: #475569; font-size: 12px;"><i class="fas fa-shopping-basket text-muted me-1"></i> {}</span>', obj.min_spend)

    @admin.display(description='Banner Tag')
    def tag_badge(self, obj):
        return format_html(
            '<span style="background-color: #f47b20; color: white; padding: 3px 8px; border-radius: 6px; font-weight: 700; font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px;">'
            '<i class="fas fa-fire me-1"></i> {}</span>',
            obj.tag
        )

    @admin.display(description='Status', ordering='is_active')
    def is_active_badge(self, obj):
        if obj.is_active:
            return mark_safe(
                '<span style="background-color: #dcfce7; color: #15803d; padding: 3px 8px; border-radius: 9999px; font-weight: 600; font-size: 11px;">'
                '<i class="fas fa-check-circle me-1"></i> Active</span>'
            )
        return mark_safe(
            '<span style="background-color: #fee2e2; color: #b91c1c; padding: 3px 8px; border-radius: 9999px; font-weight: 600; font-size: 11px;">'
            '<i class="fas fa-times-circle me-1"></i> Expired</span>'
        )

    @admin.display(description='Created On', ordering='created_at')
    def created_at_display(self, obj):
        return obj.created_at.strftime('%d %b %Y')

    # Actions
    @admin.action(description='Activate selected offers')
    def activate_offers(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"{count} offer(s) activated.")

    @admin.action(description='Deactivate selected offers')
    def deactivate_offers(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"{count} offer(s) deactivated.")
