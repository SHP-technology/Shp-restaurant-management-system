from rest_framework import serializers
from .models import Category, MenuItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'display_order', 'is_active']


class MenuItemSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    categoryId = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True,
        required=False
    )
    category_name = serializers.CharField(write_only=True, required=False)
    
    prepTime = serializers.CharField(source='prep_time', required=False)
    isVeg = serializers.BooleanField(source='is_veg', required=False)
    isSpecial = serializers.BooleanField(source='is_special', required=False)
    status = serializers.SerializerMethodField()

    class Meta:
        model = MenuItem
        fields = [
            'id',
            'name',
            'category',
            'categoryId',
            'category_name',
            'price',
            'description',
            'rating',
            'prep_time',
            'prepTime',
            'is_veg',
            'isVeg',
            'is_special',
            'isSpecial',
            'image',
            'is_in_stock',
            'status',
            'created_at',
            'updated_at',
        ]

    def get_status(self, obj):
        return 'In Stock' if obj.is_in_stock else 'Out of Stock'

    def create(self, validated_data):
        category_name = validated_data.pop('category_name', None)
        if 'category' not in validated_data and category_name:
            category, _ = Category.objects.get_or_create(name=category_name)
            validated_data['category'] = category
        elif 'category' not in validated_data:
            category, _ = Category.objects.get_or_create(name='General')
            validated_data['category'] = category
        return super().create(validated_data)
