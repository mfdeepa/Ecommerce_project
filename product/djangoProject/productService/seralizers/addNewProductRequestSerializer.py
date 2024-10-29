from rest_framework import serializers

from productService.models import Product


class AddNewProductRequestSerializer(serializers.Serializer):
    class Model:
        model = Product
        fields = ('title', 'description', 'price', 'category')

