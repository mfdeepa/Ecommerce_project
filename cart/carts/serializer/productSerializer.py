from rest_framework import serializers
from carts.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_id', 'name', 'price']
