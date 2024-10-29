from rest_framework import serializers

from productService.seralizers.productSerializer import ProductSerializer


class GetSingleProductResponseSerializer(serializers.Serializer):
    product = ProductSerializer(many=True)
