from rest_framework import viewsets, permissions
from apps.authentication.permissions import PublicActionsOrAuthenticated
from .models import TableReservation, PartyBooking
from .serializers import TableReservationSerializer, PartyBookingSerializer


class TableReservationViewSet(viewsets.ModelViewSet):
    queryset = TableReservation.objects.all()
    serializer_class = TableReservationSerializer
    permission_classes = [PublicActionsOrAuthenticated]
    # Public customers may create a reservation; staff manage the rest.
    public_actions = ['create']


class PartyBookingViewSet(viewsets.ModelViewSet):
    queryset = PartyBooking.objects.all()
    serializer_class = PartyBookingSerializer
    permission_classes = [PublicActionsOrAuthenticated]
    public_actions = ['create']
