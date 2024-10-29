from rest_framework import serializers

from productService.models import Category


class CategorySerializer(serializers.ModelSerializer):
    # def __init__(self):
    #     super(CategorySerializer, self).__init__()
    #     self.name = 'name',
    #     self.description = 'description'

    class Meta:
        model = Category
        fields = '__all__'
