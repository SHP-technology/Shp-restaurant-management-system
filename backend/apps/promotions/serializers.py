from rest_framework import serializers
from .models import Offer


class OfferSerializer(serializers.ModelSerializer):
    minSpend = serializers.CharField(source='min_spend')
    badgeColor = serializers.CharField(source='badge_color')

    class Meta:
        model = Offer
        fields = ['id', 'title', 'discount', 'minSpend', 'code', 'tag', 'badgeColor', 'is_active']
