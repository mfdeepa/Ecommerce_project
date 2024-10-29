from typing import List
from django.http import Http404
from productService.models import Category, Product
from productService.seralizers.categorySerializer import CategorySerializer
from productService.services.category_service import CategoryService
from productService.util.mapper import convert_fake_store_category_data_to_category


class CategoryServiceImpl(CategoryService):

    def get_category(self) -> List[Category]:
        categories = Category.objects.all()
        answer = []
        for category in categories:
            if isinstance(category, Category):
                answer.append(category)
            else:
                answer.append(convert_fake_store_category_data_to_category(category_data=category))
        return answer

    def get_category_by_id(self, category_id: int) -> Category:
        try:
            category = Category.objects.get(id=category_id)  # Get the category by ID
        except Category.DoesNotExist:
            raise Http404("Category not found.")
        return category

    def create_category(self, new_category) -> Category:
        category_data = {
            'name': new_category.get('name'),
            'description': new_category.get('description'),
        }

        # Pass the category data to the serializer
        serialized = CategorySerializer(data=category_data)

        if serialized.is_valid(raise_exception=True):  # Validate and raise an exception if invalid
            category = convert_fake_store_category_data_to_category(serialized.validated_data)
            category.save()
            return category
        else:
            raise ValueError("Invalid category data")

    def update_category(self, category_id: int, category_data: dict) -> Category:
        # Fetch the category by its ID, raise error if not found
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            raise Category.DoesNotExist("Category not found")

        # Pass the updated category data to the serializer and validate it
        serialized = CategorySerializer(instance=category, data=category_data, partial=True)

        if serialized.is_valid(raise_exception=True):
            # Save updated data if valid
            updated_category = serialized.save()
            return updated_category
        else:
            raise ValueError("Invalid category data")

    def delete_category(self, category_id: int) -> bool:
        try:
            category = Category.objects.get(pk=category_id)
            category.delete()
            return True
        except Category.DoesNotExist:
            raise Category.DoesNotExist("Category not found")
