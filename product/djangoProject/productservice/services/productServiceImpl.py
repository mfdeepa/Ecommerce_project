from typing import Optional, List
import httpx
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from django.http import Http404
from rest_framework.exceptions import ValidationError

from productservice.models import Product
from productservice.seralizers.productSerializer import ProductSerializer
from productservice.services.product_service import ProductService
from productservice.util.mapper import convert_fake_store_product_data_to_product


class ProductServiceImpl(ProductService):
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

    def get_all_products(self) -> List[Product]:
        products = Product.objects.all()
        answer = []
        for product in products:
            if isinstance(product, Product):
                answer.append(product)
            else:
                answer.append(convert_fake_store_product_data_to_product(product_data=product))
        return answer

    def get_single_product(self, product_id: int) -> Optional[Product]:
        try:
            product = Product.objects.get(pk=product_id)
            return product
        except Product.DoesNotExist:
            raise Http404("Product does not exist")

    def add_new_product(self, new_product, token: str) -> Product:
        user_data = self.validate_user_from_token(token)

        allowed_roles = ["Admin", "Seller"]
        user_roles = user_data.get("roles", [])
        if not any(role in allowed_roles for role in user_roles):
            raise PermissionDenied("Only Admin or Seller can add products.")

        product_data = {
            "title": new_product.get('title'),
            "description": new_product.get('description'),
            "quantity": new_product.get('quantity'),
            "price": new_product.get('price'),
        }

        serialized = ProductSerializer(data=product_data)
        if serialized.is_valid(raise_exception=True):
            product = convert_fake_store_product_data_to_product(serialized.validated_data)
            product.save()
            return product
        else:
            raise ValidationError(serialized.errors)

    def update_product(self, product_id: int, product_data: dict, token: str) -> Product:
        user_data = self.validate_user_from_token(token)
        roles = user_data.get("roles", [])

        if "customer" in [role.lower() for role in roles]:
            raise PermissionDenied("Customers are not allowed to update products.")

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise Http404("Product does not exist")

        # Validate quantity (if provided)
        quantity = product_data.get("quantity")
        if quantity is not None and int(quantity) < 1:
            raise ValidationError({"quantity": "Quantity must be at least 1."})

        serialized = ProductSerializer(instance=product, data=product_data, partial=True)
        if serialized.is_valid(raise_exception=True):
            product.title = product_data.get('title', product.title)
            product.description = product_data.get('description', product.description)
            product.price = product_data.get('price', product.price)
            product.quantity = product_data.get('quantity', product.quantity)
            product.save()
            return product
        else:
            raise ValidationError(serialized.errors)

    def delete_product(self, product_id: int, token: str):
        user_data = self.validate_user_from_token(token)
        roles = user_data.get("roles", [])

        if "customer" in [role.lower() for role in roles]:
            raise PermissionDenied("Customers are not allowed to delete products.")

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise Http404("Product not found")

        product.delete()

