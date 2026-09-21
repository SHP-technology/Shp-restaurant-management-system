from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TableReservationViewSet, PartyBookingViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'table-reservations', TableReservationViewSet, basename='table-reservation')
router.register(r'party-bookings', PartyBookingViewSet, basename='party-booking')

urlpatterns = [
    path('', include(router.urls)),
]
