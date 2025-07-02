from typing import List

import httpx
from django.http import Http404
from rest_framework.exceptions import AuthenticationFailed

from productservice.models import Category, Product
from productservice.seralizers.categorySerializer import CategorySerializer
from productservice.services.category_service import CategoryService
from productservice.util.mapper import convert_fake_store_category_data_to_category


class CategoryServiceImpl(CategoryService):
    def validate_user_from_token(self, token: str) -> dict:
        try:
            url = f"http://localhost:8001/auth/validate_token?token={token}"
            response = httpx.get(url, timeout=5.0)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 401:
                raise AuthenticationFailed("Invalid or expired token.")
            else:
                raise AuthenticationFailed(f"User validation failed with status code {response.status_code}")
        except httpx.RequestError as e:
            raise AuthenticationFailed(f"Error connecting to user service: {str(e)}")

    def get_category(self, token: str) -> List[Category]:
        self.validate_user_from_token(token)
        categories = Category.objects.all()
        return [category for category in categories]

    def get_category_by_id(self, category_id: int, token: str) -> Category:
        self.validate_user_from_token(token)
        try:
            return Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise Http404("Category not found.")

    def create_category(self, new_category: dict, token: str) -> Category:
        self.validate_user_from_token(token)

        category_data = {
            'name': new_category.get('name'),
            'description': new_category.get('description'),
        }

        serialized = CategorySerializer(data=category_data)
        if serialized.is_valid(raise_exception=True):
            category = convert_fake_store_category_data_to_category(serialized.validated_data)
            category.save()
            return category
        else:
            raise ValueError("Invalid category data")

    def update_category(self, category_id: int, category_data: dict, token: str) -> Category:
        self.validate_user_from_token(token)
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            raise Http404("Category not found")

        serialized = CategorySerializer(instance=category, data=category_data, partial=True)
        if serialized.is_valid(raise_exception=True):
            return serialized.save()
        else:
            raise ValueError("Invalid category data")

    def delete_category(self, category_id: int, token: str) -> bool:
        self.validate_user_from_token(token)
        try:
            category = Category.objects.get(pk=category_id)
            category.delete()
            return True
        except Category.DoesNotExist:
            raise Http404("Category not found")