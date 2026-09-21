from rest_framework import viewsets, permissions
from .models import RestaurantTable
from .serializers import TableSerializer


class TableViewSet(viewsets.ModelViewSet):
    queryset = RestaurantTable.objects.all()
    serializer_class = TableSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'
