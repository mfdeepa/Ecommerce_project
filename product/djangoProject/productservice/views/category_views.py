from django.http import Http404
from rest_framework import generics
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from productservice.models import Category
from productservice.seralizers.categorySerializer import CategorySerializer
from productservice.services.categoryServiceImpl import CategoryServiceImpl


class CategoryRetrieveUpdateDestroyAPIView(CreateModelMixin, generics.RetrieveUpdateDestroyAPIView):
    category_service = CategoryServiceImpl()

    def get_token(self, request):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise AuthenticationFailed("Missing or invalid Authorization header")
        return auth_header.replace("Bearer ", "").strip()

    def get(self, request, *args, **kwargs):
        token = self.get_token(request)
        category_id = kwargs.get('pk')

        if category_id:
            try:
                category = self.category_service.get_category_by_id(category_id, token)
                serializer = CategorySerializer(category)
                return Response(serializer.data, status=200)
            except Http404:
                return Response({"detail": "Category not found."}, status=404)
        else:
            categories = self.category_service.get_category(token)
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        token = self.get_token(request)
        category = self.category_service.create_category(request.data, token)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=201)

    def patch(self, request, *args, **kwargs):
        token = self.get_token(request)
        category_id = kwargs.get("pk")
        if not category_id:
            return Response({"detail": "Category ID is required in URL."}, status=400)
        try:
            category = self.category_service.update_category(category_id, request.data, token)
            serializer = CategorySerializer(category)
            return Response(serializer.data, status=200)
        except Http404:
            return Response({"detail": "Category not found."}, status=404)

    def delete(self, request, *args, **kwargs):
        token = self.get_token(request)
        category_id = kwargs.get("pk")
        if not category_id:
            return Response({"detail": "Category ID is required in URL."}, status=400)
        try:
            self.category_service.delete_category(category_id, token)
            return Response({"detail": "Category deleted successfully."}, status=204)
        except Http404:
            return Response({"detail": "Category not found."}, status=404)
