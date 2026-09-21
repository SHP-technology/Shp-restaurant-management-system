from django.contrib import admin
from django.utils.html import format_html
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        'customer_id_badge',
        'name',
        'phone_display',
        'email_display',
        'tag_badge',
        'visits_badge',
        'total_spent_badge',
        'created_at_display',
    )
    list_display_links = ('customer_id_badge', 'name')
    list_filter = ('tag', 'created_at')
    search_fields = ('id', 'name', 'phone', 'email')
    readonly_fields = ('id', 'created_at')
    ordering = ('-visits',)
    save_on_top = True

    fieldsets = (
        ('Customer Profile', {
            'fields': ('id', 'name', 'phone', 'email'),
            'classes': ('extrapretty',),
        }),
        ('Loyalty & Spending Metrics', {
            'fields': ('tag', 'visits', 'total_spent_amount'),
            'classes': ('extrapretty',),
        }),
        ('Account Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    actions = ['tag_as_vip', 'tag_as_regular', 'tag_as_new']

    @admin.display(description='Customer ID', ordering='id')
    def customer_id_badge(self, obj):
        return format_html(
            '<span style="background-color: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; padding: 2px 7px; border-radius: 6px; font-weight: 700; font-family: monospace; font-size: 11px;">'
            '<i class="fas fa-id-badge me-1"></i> {}</span>',
            obj.id
        )

    @admin.display(description='Phone Number')
    def phone_display(self, obj):
        return format_html(
            '<a href="tel:{}" style="color: #2563eb; font-weight: 500; text-decoration: none;">'
            '<i class="fas fa-phone-alt me-1 text-muted"></i> {}</a>',
            obj.phone, obj.phone
        )

    @admin.display(description='Email')
    def email_display(self, obj):
        if obj.email:
            return format_html(
                '<a href="mailto:{}" style="color: #475569; text-decoration: none;">'
                '<i class="far fa-envelope me-1 text-muted"></i> {}</a>',
                obj.email, obj.email
            )
        return format_html('<span style="color: #cbd5e1;">-</span>')

    @admin.display(description='Segment / Tier', ordering='tag')
    def tag_badge(self, obj):
        configs = {
            'VIP': ('#fef3c7', '#b45309', '#fde68a', 'fas fa-crown'),
            'Regular': ('#dbeafe', '#1d4ed8', '#bfdbfe', 'fas fa-user-check'),
            'New': ('#dcfce7', '#15803d', '#bbf7d0', 'fas fa-sparkles'),
        }
        bg, fg, border, icon = configs.get(obj.tag, ('#f3f4f6', '#374151', '#e5e7eb', 'fas fa-user'))
        return format_html(
            '<span style="background-color: {}; color: {}; border: 1px solid {}; padding: 3px 8px; border-radius: 9999px; font-weight: 700; font-size: 11px; display: inline-flex; align-items: center; gap: 4px;">'
            '<i class="{}"></i> {}</span>',
            bg, fg, border, icon, obj.tag
        )

    @admin.display(description='Dining Visits', ordering='visits')
    def visits_badge(self, obj):
        return format_html(
            '<span style="background-color: #f8fafc; color: #0f172a; border: 1px solid #e2e8f0; padding: 2px 8px; border-radius: 6px; font-weight: 700; font-size: 12px;">'
            '<i class="fas fa-utensils text-muted me-1"></i> {}</span>',
            obj.visits
        )

    @admin.display(description='Lifetime Spend', ordering='total_spent_amount')
    def total_spent_badge(self, obj):
        return format_html(
            '<span style="font-weight: 800; color: #047857; font-size: 13px;">'
            '₹{:,.2f}</span>',
            float(obj.total_spent_amount)
        )

    @admin.display(description='Registered On', ordering='created_at')
    def created_at_display(self, obj):
        return obj.created_at.strftime('%d %b %Y')

    # Actions
    @admin.action(description='Promote selected customers to VIP')
    def tag_as_vip(self, request, queryset):
        count = queryset.update(tag='VIP')
        self.message_user(request, f"{count} customer(s) promoted to VIP tier.")

    @admin.action(description='Set selected customers as Regular')
    def tag_as_regular(self, request, queryset):
        count = queryset.update(tag='Regular')
        self.message_user(request, f"{count} customer(s) updated to Regular.")

    @admin.action(description='Set selected customers as New')
    def tag_as_new(self, request, queryset):
        count = queryset.update(tag='New')
        self.message_user(request, f"{count} customer(s) marked as New.")
