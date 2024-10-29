from rest_framework import generics
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from productService.models import Category
from productService.seralizers.categorySerializer import CategorySerializer
from productService.services.categoryServiceImpl import CategoryServiceImpl


class CategoryRetrieveUpdateDestroyAPIView(CreateModelMixin, generics.RetrieveUpdateDestroyAPIView):
    category_ser = CategoryServiceImpl()

    def get(self, request, *args, **kwargs):
        categories = self.category_ser.get_category()
        category_id = self.kwargs.get('pk')
        print("Category ID:", category_id)
        if category_id:
            category = self.category_ser.get_category_by_id(category_id)
            if not category:
                return Response({"detail": "Category not found."}, status=404)
            serialized_category = CategorySerializer(category).data
        else:
            serialized_category = CategorySerializer(categories, many=True).data
        return Response(serialized_category)

    def post(self, request, *args, **kwargs):
        categories = self.category_ser.create_category(request.data)
        serialized_category = CategorySerializer(categories).data
        return Response(serialized_category)

    def patch(self, request, *args, **kwargs):
        category_id = self.kwargs.get('pk')
        if not category_id:
            return Response({"detail": "Category not found."}, status=404)
        try:
            category = self.category_ser.update_category(category_id, request.data)
        except Category.DoesNotExist:
            return Response({"detail": "Category not found."}, status=404)
        serialized_category = CategorySerializer(category, many=False).data
        return Response(serialized_category)

    def delete(self, request, *args, **kwargs):
        category_id = self.kwargs.get('pk')
        if not category_id:
            return Response({"detail": "Category not found."}, status=404)
        category = self.category_ser.delete_category(category_id)
        if category:
            return Response({"detail": "Category deleted successfully."}, status=200)
        else:
            return Response({"detail": "Category not found."}, status=404)
