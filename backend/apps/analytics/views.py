import csv
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Avg
from apps.orders.models import Order, OrderType
from apps.reservations.models import TableReservation, PartyBooking
from apps.tables.models import RestaurantTable
from apps.menu.models import MenuItem


class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from django.utils import timezone

        today = timezone.now().date()
        today_orders = Order.objects.filter(created_at__date=today).count()
        table_bookings = TableReservation.objects.count()
        delivery_orders = Order.objects.filter(order_type=OrderType.DELIVERY).count()
        party_bookings = PartyBooking.objects.count()

        today_revenue = Order.objects.filter(created_at__date=today).aggregate(
            total=Sum('total_amount'))['total'] or 0
        total_revenue = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0
        aov = Order.objects.aggregate(avg=Avg('total_amount'))['avg'] or 0

        stats = [
            {'label': "Today's Orders", 'value': f"{today_orders:02d}"},
            {'label': 'Table Bookings', 'value': f"{table_bookings:02d}"},
            {'label': 'Delivery Orders', 'value': f"{delivery_orders:02d}"},
            {'label': 'Party Bookings', 'value': f"{party_bookings:02d}"},
        ]

        reports = {
            'totalRevenue': f"₹{int(total_revenue):,}",
            'averageOrderValue': f"₹{int(aov):,}",
            'todayRevenue': f"₹{int(today_revenue):,}",
        }

        return Response({
            'stats': stats,
            'reports': reports,
        })


class ExportReportCSVView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="shp_restaurant_sales_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Order ID', 'Order Type', 'Customer / Table', 'Total Amount', 'Status', 'Date'])

        for o in Order.objects.all():
            writer.writerow([
                o.id,
                o.order_type,
                o.customer_display,
                f"₹{int(o.total_amount)}",
                o.status,
                o.created_at.strftime('%Y-%m-%d %H:%M')
            ])

        return response
