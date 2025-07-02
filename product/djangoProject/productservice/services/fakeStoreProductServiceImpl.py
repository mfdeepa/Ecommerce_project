from typing import Optional, List

import httpx
import injector
from rest_framework.exceptions import ValidationError

from productservice.clients.fakeStoreClient.fakeStoreClient import FakeStoreClient
from productservice.models import Product, Category
from productservice.seralizers.productSerializer import ProductSerializer
from productservice.services.product_service import ProductService
from productservice.util.mapper import convert_fake_store_product_data_to_product


class FakeStoreProductServiceImpl(ProductService):

    @injector.inject
    def __init__(self):
        self.http_client = httpx.Client
        self.fake_store_client = FakeStoreClient()

    def get_all_products(self) -> List[Product]:
        fake_store_products = self.fake_store_client.get_all_products()

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
            print(f"Error converting productservice data for ID {product_id}: {str(e)}")
            raise ValidationError('Error processing productservice data')  # Proper error handling

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



