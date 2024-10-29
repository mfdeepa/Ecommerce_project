from typing import Optional, List

import httpx
import injector
from rest_framework.exceptions import ValidationError

from productService.clients.fakeStoreClient.fakeStoreClient import FakeStoreClient
from productService.models import Product, Category
from productService.seralizers.productSerializer import ProductSerializer
from productService.services.product_service import ProductService
from productService.util.mapper import convert_fake_store_product_data_to_product


class FakeStoreProductServiceImpl(ProductService):

    @injector.inject
    def __init__(self):
        self.http_client = httpx.Client
        self.fake_store_client = FakeStoreClient()

    # @injector.inject
    # def convert_fake_store_product_data_to_product(self, product_data: dict) -> Product:
    #     if product_data is None:
    #         print("Received None for product_data")
    #         raise ValidationError("Product data is invalid")
    #     category_name = product_data.get('category', 'Unknown')
    #     category, created = Category.objects.get_or_create(name=category_name)
    #
    #     # Convert external API data to your Django model instance
    #     product = Product.objects.create(
    #         title=product_data['title'],
    #         price=product_data['price'],
    #         description=product_data.get('description', ''),
    #         category=category,
    #     )
    #     return product

    def get_all_products(self) -> List[Product]:
        # Get product data from the external API
        fake_store_products = self.fake_store_client.get_all_products()

        # Convert the data into Product instances
        answer = []
        for product_data in fake_store_products:
            answer.append(convert_fake_store_product_data_to_product(product_data))

        return answer

    def get_single_product(self, product_id: int) -> Optional[Product]:
        fake_store_product = self.fake_store_client.get_single_product(product_id)

        if not fake_store_product:
            print(f"Product with ID {product_id} not found in external store.")
            raise ValidationError('Product not found')  # Return 404 or appropriate error response

        try:
            answer = convert_fake_store_product_data_to_product(fake_store_product)
            return answer
        except AttributeError as e:
            print(f"Error converting product data for ID {product_id}: {str(e)}")
            raise ValidationError('Error processing product data')  # Proper error handling

    def add_new_product(self, product: ProductSerializer) -> Product:
        fake_store_products = self.fake_store_client.add_new_product(product)
        answer = convert_fake_store_product_data_to_product(fake_store_products)
        answer.save()
        return answer

    def update_product(self, product_id: int, product: Product) -> Product:
        fake_store_products = self.fake_store_client.update_product(product_id, product)
        answer = convert_fake_store_product_data_to_product(fake_store_products)
        answer.save()
        return answer

    def delete_product(self, product_id: int) -> bool:
        answer = self.fake_store_client.delete_product(product_id)
        # answer.save()
        return True if answer is None else False

    def get_limit_product_result(self, limit: int, offset: int):
        pass

    def update_product_partially(self, product_id: int) -> str:
        # django update method cal the partial update method so no need to repeat
        pass

    def get_product_by_sorting(self, product_id: int) -> str:
        pass

