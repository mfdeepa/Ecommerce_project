from rest_framework import serializers

from productservice.models import Category


class FakeStoreCategorySerializer(serializers.ModelSerializer):
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')
        super().__init__(**kwargs)

    class Meta:
        model = Category
        fields = '__all__'
