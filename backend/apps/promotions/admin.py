from django.contrib import admin
from django.utils.html import format_html
from .models import Offer


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'discount', 'min_spend', 'tag_badge', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    list_editable = ('is_active',)
    search_fields = ('code', 'title', 'discount')
    readonly_fields = ('created_at',)

    @admin.display(description='Tag')
    def tag_badge(self, obj):
        return format_html(
            '<span style="background-color: #f47b20; color: white; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 10px;">{}</span>',
            obj.tag
        )
