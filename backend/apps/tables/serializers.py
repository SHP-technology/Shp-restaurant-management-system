from rest_framework import serializers
from .models import RestaurantTable


class TableSerializer(serializers.ModelSerializer):
    num = serializers.IntegerField(source='table_number', required=False)

    class Meta:
        model = RestaurantTable
        fields = ['id', 'num', 'table_number', 'seats', 'status', 'floor_zone', 'updated_at']

    def create(self, validated_data):
        if 'table_number' not in validated_data and 'num' in validated_data:
            validated_data['table_number'] = validated_data.pop('num')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'table_number' not in validated_data and 'num' in validated_data:
            validated_data['table_number'] = validated_data.pop('num')
        return super().update(instance, validated_data)
