from typing import Optional, List

from django.http import Http404
from rest_framework.exceptions import ValidationError

from productService.models import Product
from productService.seralizers.productSerializer import ProductSerializer
from productService.services.product_service import ProductService
from productService.util.mapper import convert_fake_store_product_data_to_product


class ProductServiceImpl(ProductService):
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

    def add_new_product(self, new_product) -> Product:
        product_data = {
            "title": new_product.get('title'),
            "description": new_product.get('description'),
            "price": new_product.get('price'),
        }

        serialized = ProductSerializer(data=product_data)
        if serialized.is_valid(raise_exception=True):
            product = convert_fake_store_product_data_to_product(serialized.validated_data)
            product.save()
            return product
        else:
            raise ValidationError(serialized.errors)

    def update_product(self, product_id: int, product_data: dict) -> Product:
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            raise Http404("Product does not exist")

        serialized = ProductSerializer(instance=product, data=product_data, partial=True)
        if serialized.is_valid(raise_exception=True):
            product.title = product_data.get('title')
            product.description = product_data.get('description')
            product.price = product_data.get('price')
            product.save()
            return product
        else:
            raise ValidationError(serialized.errors)

    def delete_product(self, product_id: int) -> bool:
        try:
            product = Product.objects.get(pk=product_id)
            product.delete()
            return True
        except Product.DoesNotExist:
            raise False

    def get_limit_product_result(self, limit: int, offset: int) -> str:
        pass

    def get_product_by_sorting(self, product_id: int) -> str:
        pass

    def update_product_partially(self, product_id: int) -> str:
        # update product has a partially updated product function, so no need to create duplicate method.
        pass
