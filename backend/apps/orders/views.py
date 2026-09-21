from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'pk'
    lookup_value_regex = r'[^/]+'

    def get_queryset(self):
        queryset = super().get_queryset()
        order_type = self.request.query_params.get('type')
        status_param = self.request.query_params.get('status')

        if order_type and order_type != 'All':
            queryset = queryset.filter(order_type=order_type)
        if status_param and status_param != 'All':
            queryset = queryset.filter(status=status_param)

        return queryset

    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get('status')
        if not new_status:
            return Response(
                {'detail': 'Status field is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        order.status = new_status
        order.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
