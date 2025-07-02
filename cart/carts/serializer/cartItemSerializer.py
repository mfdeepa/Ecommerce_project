from rest_framework import serializers
from carts.models import CartItem, Product

class CartItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    subtotal = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True, source='get_subtotal'
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'title', 'quantity', 'price', 'subtotal']
        read_only_fields = ['subtotal']

    def validate(self, data):
        if data.get("price") is None or data.get("title") is None:
            raise serializers.ValidationError("Both title and price must be provided.")
        return data

