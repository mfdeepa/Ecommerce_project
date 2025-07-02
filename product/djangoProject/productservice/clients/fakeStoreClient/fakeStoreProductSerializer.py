from rest_framework import serializers

from productservice.models import Product
from productservice.seralizers.ratingSerializer import RatingSerializer


class FakeStoreProductSerializer(serializers.ModelSerializer):
    rating = RatingSerializer()

    def __init__(self, **kwargs):
        self.id = kwargs.pop('id', None)
        self.title = kwargs.pop('title', None)
        self.description = kwargs.pop('description', None)
        self.price = kwargs.pop('price', None)
        self.category = kwargs.pop('category', None)
        self.rating = kwargs.pop('rating', None)
        super(FakeStoreProductSerializer, self).__init__(**kwargs)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category', 'rating']
