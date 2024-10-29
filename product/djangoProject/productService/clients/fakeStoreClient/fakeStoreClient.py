from typing import List, Optional

import httpx
import injector

from productService.clients.fakeStoreClient.FakeStoreCategorySerializer import FakeStoreCategorySerializer
from productService.clients.fakeStoreClient.fakeStoreProductSerializer import FakeStoreProductSerializer
from productService.models import Product
from productService.seralizers.productSerializer import ProductSerializer


class FakeStoreClient:
    BASE_URL = "https://fakestoreapi.com"

    @injector.inject
    def __init__(self):
        self.client = httpx.Client()
        self.fake_store_product_serializer = FakeStoreProductSerializer()

    def get_all_products(self) -> List[FakeStoreProductSerializer]:
        response = self.client.get(f"{"https://fakestoreapi.com"}/products")  # this will give me JSON response
        response.raise_for_status()
        product_data = response.json()  # convert JSON into an object
        return product_data

    def get_single_product(self, product_id: int) -> Optional[FakeStoreProductSerializer]:
        response = self.client.get(f"{self.BASE_URL}/products/{product_id}")

        if response.status_code != 200:
            print(f"Product with ID {product_id} not found. Status code: {response.status_code}")
            return None

        # Check if the response body is empty
        if not response.text.strip():  # Empty body check
            print(f"Received empty response body for product ID {product_id}")
            return None

        # Check if the response contains valid JSON
        try:
            product_data = response.json()
            if not product_data:
                print(f"Received empty product data for product ID {product_id}")
                return None
            return product_data
        except ValueError as e:
            print(f"Error parsing JSON for product ID {product_id}: {str(e)}")
            return None

    def add_new_product(self, product: ProductSerializer) -> FakeStoreProductSerializer:
        response = self.client.post(f"{"https://fakestoreapi.com"}/products", json=product)
        response.raise_for_status()
        product_data = response.json()  # convert JSON into an object
        return product_data

    def update_product(self, product_id: int, product: Product) -> FakeStoreProductSerializer:
        product_data = {
            "category": product.get('category', 'Unknown'),
            "title": product.get('title', ''),
            "description": product.get('description', ''),
            "price": product.get('price', 0),
        }
        response = self.client.patch(f"{"https://fakestoreapi.com"}/products/{product_id}", json=product_data)

        response.raise_for_status()
        product_data = response.json()
        return product_data

    def delete_product(self, product_id: int) -> None:
        response = self.client.delete(f"{"https://fakestoreapi.com"}/products/{product_id}")
        response.raise_for_status()
        return None

    def get_limit_product_result(self) -> List[FakeStoreProductSerializer]:
        response = self.client.get(f"{"https://fakestoreapi.com"}/products")
        response.raise_for_status()
        product_data = response.json()
        return product_data

    def update_product_partially(self, product_id: int) -> FakeStoreProductSerializer:
        #django update_product function call the partial update function so no need to create seperate method
        #for partially update
        pass

    def get_product_by_sorting(self, product_id: int) -> FakeStoreProductSerializer:
        pass

    def get_all_categories(self) -> List[FakeStoreCategorySerializer]:
        response = self.client.get(f"{self.BASE_URL}/products/categories")
        response.raise_for_status()
        category_data = response.json()  # convert JSON into a Python list of dictionaries
        return category_data

    def get_in_category(self) -> List[FakeStoreCategorySerializer]:
        response = self.client.get(f"{self.BASE_URL}/products/category/")
        response.raise_for_status()
        category_data = response.json()
        return category_data

    # def create_category(self, category: CategorySerializer) -> FakeStoreCategorySerializer:
    # create category is not allowed in fake store api

    # def update_category(self, category_request_serializer):
    # update category is also not a part of fake store api

    # def delete_category(self, category_request_serializer) -> bool:
    # delete category is not a part of fake store api
