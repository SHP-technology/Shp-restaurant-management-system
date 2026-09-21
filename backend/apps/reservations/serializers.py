from rest_framework import serializers
from .models import TableReservation, PartyBooking


class TableReservationSerializer(serializers.ModelSerializer):
    timeSlot = serializers.CharField(source='time', required=False)
    seatingZone = serializers.CharField(source='area', required=False)
    specialRequest = serializers.CharField(source='special_request', required=False, allow_blank=True)

    class Meta:
        model = TableReservation
        fields = [
            'id',
            'name',
            'phone',
            'date',
            'time',
            'timeSlot',
            'guests',
            'area',
            'seatingZone',
            'special_request',
            'specialRequest',
            'status',
            'assigned_table',
            'created_at',
        ]

    def create(self, validated_data):
        if 'guests' in validated_data and str(validated_data['guests']).isdigit():
            validated_data['guests'] = f"{validated_data['guests']} People"
        return super().create(validated_data)


class PartyBookingSerializer(serializers.ModelSerializer):
    guestCount = serializers.CharField(source='guests', required=False)
    clientName = serializers.CharField(source='client', required=False)

    class Meta:
        model = PartyBooking
        fields = [
            'id',
            'occasion',
            'client',
            'clientName',
            'phone',
            'date',
            'guests',
            'guestCount',
            'requirements',
            'status',
            'created_at',
        ]
