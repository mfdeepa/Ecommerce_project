from rest_framework import serializers
from carts.models import Discount


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = [
            'id', 'code', 'discount_type', 'value',
            'min_purchase_amount', 'valid_from',
            'valid_until', 'max_uses', 'current_uses'
        ]
