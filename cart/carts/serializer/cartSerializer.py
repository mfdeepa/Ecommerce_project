from rest_framework import serializers

from carts.models import Cart
from carts.serializer.cartItemSerializer import CartItemSerializer


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True, source='get_subtotal')
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True, source='get_total')
    discount_code = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'subtotal', 'total', 'discount_code', 'expires_at']
