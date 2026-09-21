from django.contrib import admin
from django.utils.html import format_html
from .models import TableReservation, PartyBooking


@admin.register(TableReservation)
class TableReservationAdmin(admin.ModelAdmin):
    list_display = (
        'reservation_id_badge',
        'guest_info',
        'schedule_badge',
        'guests_badge',
        'area_badge',
        'table_assignment_badge',
        'status_badge',
        'created_at_display',
    )
    list_display_links = ('reservation_id_badge', 'guest_info')
    list_filter = ('status', 'area', 'date', 'created_at')
    search_fields = ('id', 'name', 'phone', 'special_request', 'area')
    readonly_fields = ('id', 'created_at')
    save_on_top = True

    fieldsets = (
        ('Reservation Details', {
            'fields': ('id', 'name', 'phone', 'status'),
            'classes': ('extrapretty',),
        }),
        ('Schedule & Seating Preferences', {
            'fields': ('date', 'time', 'guests', 'area', 'assigned_table'),
            'classes': ('extrapretty',),
        }),
        ('Guest Notes & Requests', {
            'fields': ('special_request',),
            'classes': ('extrapretty',),
        }),
        ('Audit Log', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    actions = ['mark_confirmed', 'mark_pending', 'mark_cancelled']

    @admin.display(description='Booking ID', ordering='id')
    def reservation_id_badge(self, obj):
        return format_html(
            '<span style="background-color: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; padding: 3px 8px; border-radius: 6px; font-weight: 700; font-family: monospace; font-size: 12px;">'
            '<i class="fas fa-calendar-check me-1"></i> {}</span>',
            obj.id
        )

    @admin.display(description='Guest')
    def guest_info(self, obj):
        return format_html(
            '<div>'
            '<div style="font-weight: 600; color: #0f172a;">{}</div>'
            '<div style="font-size: 11px; color: #64748b;"><i class="fas fa-phone-alt me-1"></i> {}</div>'
            '</div>',
            obj.name, obj.phone
        )

    @admin.display(description='Date & Time')
    def schedule_badge(self, obj):
        return format_html(
            '<span style="background-color: #f1f5f9; color: #334155; padding: 3px 8px; border-radius: 6px; font-weight: 600; font-size: 11px; white-space: nowrap;">'
            '<i class="far fa-calendar-alt text-primary me-1"></i> {} <span style="color: #94a3b8;">•</span> {}</span>',
            obj.date, obj.time
        )

    @admin.display(description='Party Size')
    def guests_badge(self, obj):
        return format_html(
            '<span style="background-color: #e0f2fe; color: #0369a1; padding: 2px 8px; border-radius: 9999px; font-weight: 600; font-size: 11px;">'
            '<i class="fas fa-users me-1"></i> {}</span>',
            obj.guests
        )

    @admin.display(description='Seating Area')
    def area_badge(self, obj):
        return format_html(
            '<span style="background-color: #f3f4f6; color: #4b5563; padding: 2px 8px; border-radius: 6px; font-size: 12px;">'
            '<i class="fas fa-map-pin text-muted me-1"></i> {}</span>',
            obj.area
        )

    @admin.display(description='Assigned Table')
    def table_assignment_badge(self, obj):
        if obj.assigned_table:
            return format_html(
                '<span style="font-weight: 600; color: #1e293b;"><i class="fas fa-chair text-success me-1"></i> Table #{}</span>',
                obj.assigned_table.table_number
            )
        return format_html('<span style="color: #94a3b8; font-style: italic;">Auto / Unassigned</span>')

    @admin.display(description='Status', ordering='status')
    def status_badge(self, obj):
        colors = {
            'Confirmed': ('#dcfce7', '#15803d', 'fas fa-check-circle'),
            'Pending': ('#fef3c7', '#b45309', 'fas fa-clock'),
            'Cancelled': ('#fee2e2', '#991b1b', 'fas fa-times-circle'),
        }
        bg, fg, icon = colors.get(obj.status, ('#f3f4f6', '#374151', 'fas fa-info-circle'))
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 4px 10px; border-radius: 9999px; font-weight: 600; font-size: 11px; display: inline-flex; align-items: center; gap: 4px;">'
            '<i class="{}"></i> {}</span>',
            bg, fg, icon, obj.status
        )

    @admin.display(description='Booked At', ordering='created_at')
    def created_at_display(self, obj):
        return obj.created_at.strftime('%d %b, %I:%M %p')

    # Actions
    @admin.action(description='Mark selected reservations as Confirmed')
    def mark_confirmed(self, request, queryset):
        count = queryset.update(status='Confirmed')
        self.message_user(request, f"{count} reservation(s) marked as Confirmed.")

    @admin.action(description='Mark selected reservations as Pending')
    def mark_pending(self, request, queryset):
        count = queryset.update(status='Pending')
        self.message_user(request, f"{count} reservation(s) marked as Pending.")

    @admin.action(description='Mark selected reservations as Cancelled')
    def mark_cancelled(self, request, queryset):
        count = queryset.update(status='Cancelled')
        self.message_user(request, f"{count} reservation(s) marked as Cancelled.")


@admin.register(PartyBooking)
class PartyBookingAdmin(admin.ModelAdmin):
    list_display = (
        'booking_id_badge',
        'occasion_badge',
        'client_info',
        'event_date_badge',
        'guests_count_badge',
        'status_badge',
        'requirements_display',
        'created_at_display',
    )
    list_display_links = ('booking_id_badge', 'client_info')
    list_filter = ('occasion', 'status', 'date', 'created_at')
    search_fields = ('id', 'client', 'phone', 'occasion', 'requirements')
    readonly_fields = ('id', 'created_at')
    save_on_top = True

    fieldsets = (
        ('Event Booking Details', {
            'fields': ('id', 'occasion', 'client', 'phone', 'status'),
            'classes': ('extrapretty',),
        }),
        ('Party Logistics & Requirements', {
            'fields': ('date', 'guests', 'requirements'),
            'classes': ('extrapretty',),
        }),
        ('Audit Log', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )

    actions = ['mark_confirmed', 'mark_pending_inquiry', 'mark_cancelled']

    @admin.display(description='Event ID', ordering='id')
    def booking_id_badge(self, obj):
        return format_html(
            '<span style="background-color: #faf5ff; color: #7e22ce; border: 1px solid #e9d5ff; padding: 3px 8px; border-radius: 6px; font-weight: 700; font-family: monospace; font-size: 12px;">'
            '<i class="fas fa-glass-cheers me-1"></i> {}</span>',
            obj.id
        )

    @admin.display(description='Occasion', ordering='occasion')
    def occasion_badge(self, obj):
        return format_html(
            '<span style="background-color: #fff1f2; color: #be123c; padding: 3px 8px; border-radius: 6px; font-weight: 600; font-size: 12px;">'
            '<i class="fas fa-birthday-cake me-1"></i> {}</span>',
            obj.occasion
        )

    @admin.display(description='Client')
    def client_info(self, obj):
        phone_html = f'<div style="font-size: 11px; color: #64748b;"><i class="fas fa-phone-alt me-1"></i> {obj.phone}</div>' if obj.phone else ''
        return format_html(
            '<div>'
            '<div style="font-weight: 600; color: #0f172a;">{}</div>'
            '{}'
            '</div>',
            obj.client, format_html(phone_html)
        )

    @admin.display(description='Event Date')
    def event_date_badge(self, obj):
        return format_html(
            '<span style="background-color: #f1f5f9; color: #334155; padding: 3px 8px; border-radius: 6px; font-weight: 600; font-size: 11px;">'
            '<i class="far fa-calendar-alt text-primary me-1"></i> {}</span>',
            obj.date
        )

    @admin.display(description='Expected Guests')
    def guests_count_badge(self, obj):
        return format_html(
            '<span style="background-color: #e0f2fe; color: #0369a1; padding: 2px 8px; border-radius: 9999px; font-weight: 600; font-size: 11px;">'
            '<i class="fas fa-users me-1"></i> {}</span>',
            obj.guests
        )

    @admin.display(description='Requirements')
    def requirements_display(self, obj):
        summary = obj.requirements[:40] + '...' if len(obj.requirements) > 40 else obj.requirements
        return format_html('<span style="color: #475569; font-size: 12px;" title="{}">{}</span>', obj.requirements, summary or 'None')

    @admin.display(description='Status', ordering='status')
    def status_badge(self, obj):
        colors = {
            'Confirmed': ('#dcfce7', '#15803d', 'fas fa-check-circle'),
            'Pending Inquiry': ('#ffedd5', '#c2410c', 'fas fa-clock'),
            'Cancelled': ('#fee2e2', '#991b1b', 'fas fa-times-circle'),
        }
        bg, fg, icon = colors.get(obj.status, ('#f3f4f6', '#374151', 'fas fa-info-circle'))
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 4px 10px; border-radius: 9999px; font-weight: 600; font-size: 11px; display: inline-flex; align-items: center; gap: 4px;">'
            '<i class="{}"></i> {}</span>',
            bg, fg, icon, obj.status
        )

    @admin.display(description='Created On', ordering='created_at')
    def created_at_display(self, obj):
        return obj.created_at.strftime('%d %b %Y')

    # Actions
    @admin.action(description='Mark selected bookings as Confirmed')
    def mark_confirmed(self, request, queryset):
        count = queryset.update(status='Confirmed')
        self.message_user(request, f"{count} event booking(s) marked as Confirmed.")

    @admin.action(description='Mark selected bookings as Pending Inquiry')
    def mark_pending_inquiry(self, request, queryset):
        count = queryset.update(status='Pending Inquiry')
        self.message_user(request, f"{count} event booking(s) updated to Pending Inquiry.")

    @admin.action(description='Mark selected bookings as Cancelled')
    def mark_cancelled(self, request, queryset):
        count = queryset.update(status='Cancelled')
        self.message_user(request, f"{count} event booking(s) marked as Cancelled.")
