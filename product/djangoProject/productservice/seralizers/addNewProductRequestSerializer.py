from rest_framework import serializers

from productservice.models import Product


class AddNewProductRequestSerializer(serializers.Serializer):
    class Model:
        model = Product
        fields = ('title', 'description', 'price', 'category')

