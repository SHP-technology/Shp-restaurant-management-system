from rest_framework import viewsets, permissions
from .models import TableReservation, PartyBooking
from .serializers import TableReservationSerializer, PartyBookingSerializer


class TableReservationViewSet(viewsets.ModelViewSet):
    queryset = TableReservation.objects.all()
    serializer_class = TableReservationSerializer
    permission_classes = [permissions.AllowAny]


class PartyBookingViewSet(viewsets.ModelViewSet):
    queryset = PartyBooking.objects.all()
    serializer_class = PartyBookingSerializer
    permission_classes = [permissions.AllowAny]
