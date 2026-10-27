from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Restaurant
from .serializers import RestaurantSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'])
    def current(self, request):
        restaurant = Restaurant.objects.filter(is_active=True).first() or Restaurant.objects.first()
        if not restaurant:
            restaurant = Restaurant.objects.create(
                name="SHP Restaurant",
                tagline="Good Food Great Moments",
                outlet_name="SHP Restaurant - Civil Lines"
            )
        serializer = self.get_serializer(restaurant)
        return Response(serializer.data)
