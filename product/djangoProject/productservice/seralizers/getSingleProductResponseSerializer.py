from rest_framework import serializers

from productservice.seralizers.productSerializer import ProductSerializer


class GetSingleProductResponseSerializer(serializers.Serializer):
    product = ProductSerializer(many=True)
