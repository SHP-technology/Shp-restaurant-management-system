from rest_framework import serializers
from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    totalSpent = serializers.CharField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone', 'email', 'tag', 'visits', 'total_spent_amount', 'totalSpent', 'created_at']
