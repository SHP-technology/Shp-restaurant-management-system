from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import User, Role


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'email',
        'name',
        'role_badge',
        'restaurant_display',
        'phone',
        'is_staff_badge',
        'is_active_badge',
        'created_at_display',
    )
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'restaurant', 'created_at')
    search_fields = ('email', 'name', 'phone', 'restaurant__name')
    ordering = ('-created_at',)
    save_on_top = True

    fieldsets = (
        (_('Credentials & Authentication'), {
            'fields': ('email', 'password'),
            'classes': ('extrapretty',),
        }),
        (_('Personal Information'), {
            'fields': ('name', 'phone', 'restaurant'),
            'classes': ('extrapretty',),
        }),
        (_('Role & Access Permissions'), {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('extrapretty',),
        }),
        (_('Activity & Timestamps'), {
            'fields': ('last_login', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at', 'last_login')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'name', 'role', 'restaurant', 'phone', 'is_staff', 'is_active'),
        }),
    )

    actions = [
        'make_admin',
        'make_manager',
        'make_waiter',
        'make_kitchen',
        'activate_users',
        'deactivate_users',
    ]

    @admin.display(description='Role', ordering='role')
    def role_badge(self, obj):
        colors = {
            'admin': ('#dc2626', 'fas fa-crown'),
            'manager': ('#ea580c', 'fas fa-user-tie'),
            'waiter': ('#2563eb', 'fas fa-concierge-bell'),
            'kitchen': ('#7c3aed', 'fas fa-utensils'),
            'customer': ('#059669', 'fas fa-user'),
        }
        color, icon = colors.get(obj.role, ('#4b5563', 'fas fa-user-circle'))
        display_label = obj.get_role_display() if hasattr(obj, 'get_role_display') else obj.role
        return format_html(
            '<span style="display: inline-flex; align-items: center; gap: 5px; background-color: {}; '
            'color: #fff; padding: 4px 10px; border-radius: 9999px; font-weight: 600; font-size: 11px; '
            'box-shadow: 0 1px 2px rgba(0,0,0,0.1);">'
            '<i class="{}"></i> {}</span>',
            color, icon, display_label
        )

    @admin.display(description='Restaurant Outlet')
    def restaurant_display(self, obj):
        if obj.restaurant:
            return format_html(
                '<span style="font-weight: 500; color: #1e293b;"><i class="fas fa-store text-muted me-1"></i> {}</span>',
                obj.restaurant.outlet_name
            )
        return mark_safe('<span style="color: #94a3b8; font-style: italic;">All Outlets / HQ</span>')

    @admin.display(description='Staff', boolean=False)
    def is_staff_badge(self, obj):
        if obj.is_staff:
            return mark_safe('<span style="color: #16a34a; font-weight: 600;"><i class="fas fa-check-circle"></i> Yes</span>')
        return mark_safe('<span style="color: #94a3b8;"><i class="fas fa-minus-circle"></i> No</span>')

    @admin.display(description='Status', boolean=False)
    def is_active_badge(self, obj):
        if obj.is_active:
            return mark_safe('<span style="background-color: #dcfce7; color: #15803d; padding: 2px 8px; border-radius: 6px; font-weight: 600; font-size: 11px;">Active</span>')
        return mark_safe('<span style="background-color: #fee2e2; color: #b91c1c; padding: 2px 8px; border-radius: 6px; font-weight: 600; font-size: 11px;">Inactive</span>')

    @admin.display(description='Joined On', ordering='created_at')
    def created_at_display(self, obj):
        return obj.created_at.strftime('%d %b %Y, %I:%M %p')

    # Bulk actions
    @admin.action(description='Mark selected users as Active')
    def activate_users(self, request, queryset):
        count = queryset.update(is_active=True)
        self.message_user(request, f"{count} user(s) successfully activated.")

    @admin.action(description='Mark selected users as Inactive')
    def deactivate_users(self, request, queryset):
        count = queryset.update(is_active=False)
        self.message_user(request, f"{count} user(s) deactivated.")

    @admin.action(description='Set Role: Admin')
    def make_admin(self, request, queryset):
        count = queryset.update(role=Role.ADMIN, is_staff=True)
        self.message_user(request, f"{count} user(s) updated to Admin.")

    @admin.action(description='Set Role: Manager')
    def make_manager(self, request, queryset):
        count = queryset.update(role=Role.MANAGER, is_staff=True)
        self.message_user(request, f"{count} user(s) updated to Manager.")

    @admin.action(description='Set Role: Waiter')
    def make_waiter(self, request, queryset):
        count = queryset.update(role=Role.WAITER, is_staff=True)
        self.message_user(request, f"{count} user(s) updated to Waiter.")

    @admin.action(description='Set Role: Kitchen Staff')
    def make_kitchen(self, request, queryset):
        count = queryset.update(role=Role.KITCHEN, is_staff=True)
        self.message_user(request, f"{count} user(s) updated to Kitchen Staff.")
