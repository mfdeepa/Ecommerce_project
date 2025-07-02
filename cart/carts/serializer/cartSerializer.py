from rest_framework import serializers
from carts.models import Cart, Discount
from carts.serializer.cartItemSerializer import CartItemSerializer


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True, source='get_subtotal')
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True, source='get_total')
    discount_code = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Cart
        fields = ['id', 'items', 'subtotal', 'total', 'discount_code', 'expires_at']

    def update(self, instance, validated_data):
        discount_code = validated_data.pop('discount_code', None)
        if discount_code:
            try:
                discount = Discount.objects.get(code=discount_code)
                instance.discount = discount
                instance.save()
            except Discount.DoesNotExist:
                raise serializers.ValidationError({'discount_code': 'Invalid discount code.'})
        return instance
