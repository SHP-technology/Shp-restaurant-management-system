from django.contrib import admin
from django.utils.html import format_html
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'tag_badge', 'visits', 'total_spent_display', 'created_at')
    list_filter = ('tag', 'created_at')
    list_editable = ()
    search_fields = ('id', 'name', 'phone', 'email')
    readonly_fields = ('id', 'created_at')
    ordering = ('-visits',)

    @admin.display(description='Total Spent')
    def total_spent_display(self, obj):
        return f"₹{int(obj.total_spent_amount):,}"

    @admin.display(description='Segment')
    def tag_badge(self, obj):
        colors = {
            'VIP': ('#fef3c7', '#b45309'),
            'Regular': ('#dbeafe', '#1d4ed8'),
            'New': ('#dcfce7', '#15803d'),
        }
        bg, fg = colors.get(obj.tag, ('#f3f4f6', '#374151'))
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 3px 8px; border-radius: 4px; font-weight: bold; font-size: 11px;">{}</span>',
            bg, fg, obj.tag
        )
