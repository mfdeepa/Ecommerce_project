from rest_framework import serializers

from carts.models import CartItem, Product
from carts.serializer.productSerializer import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True, source='get_subtotal')

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'subtotal']

    def validate(self, data):
        try:
            product = Product.objects.get(pk=data['product_id'])
            if not product.check_inventory(data['quantity']):
                raise serializers.ValidationError(
                    f"Insufficient inventory. Only {product.inventory_count} available."
                )
            data['price'] = product.price
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found")
        return data
