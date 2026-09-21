from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        search = self.request.query_params.get('search')
        veg_only = self.request.query_params.get('veg_only')

        if category and category != 'All':
            queryset = queryset.filter(category__name__iexact=category)
        if search:
            queryset = queryset.filter(name__icontains=search) | queryset.filter(description__icontains=search)
        if veg_only in ['true', 'True', '1']:
            queryset = queryset.filter(is_veg=True)

        return queryset

    @action(detail=True, methods=['patch'], url_path='toggle-stock')
    def toggle_stock(self, request, pk=None):
        item = self.get_object()
        item.is_in_stock = not item.is_in_stock
        item.save()
        return Response(MenuItemSerializer(item).data)
