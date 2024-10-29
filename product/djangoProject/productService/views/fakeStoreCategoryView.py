from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response

from productService.seralizers.categorySerializer import CategorySerializer
from productService.services.fakeStoreCategoryServiceImpl import FakeStoreCategoryServiceImpl


class FakeStoreCategoryListCreateAPIView(ListCreateAPIView):  # this will cal when we want to fetch fakeStoreApi
    category_ser = FakeStoreCategoryServiceImpl()

    def get(self, request, *args, **kwargs):  # this will use only, when we want to fetch fakeStoreApi data only
        categories = self.category_ser.get_all_categories()
        serialized_category = CategorySerializer(categories, many=True).data
        return Response(serialized_category)


class FakeStoreCategoryRetrieveAPIView(RetrieveAPIView):
    category_ser = FakeStoreCategoryServiceImpl()

    def get(self, request, *args, **kwargs):
        category_name = self.kwargs.get('name')
        categories = self.category_ser.get_in_category(category_name)
        serialized_category = CategorySerializer(categories, many=True).data
        return Response(serialized_category)
