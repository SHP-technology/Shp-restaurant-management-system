from django.urls import re_path
from .views import DashboardStatsView, ExportReportCSVView

urlpatterns = [
    re_path(r'^dashboard/?$', DashboardStatsView.as_view(), name='analytics_dashboard'),
    re_path(r'^export-csv/?$', ExportReportCSVView.as_view(), name='analytics_export_csv'),
]
