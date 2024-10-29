from typing import List

import httpx
import injector

from productService.clients.fakeStoreClient.fakeStoreClient import FakeStoreClient
from productService.models import Category
from productService.services.fakeStoreCategoryService import FakeStoreCategoryService
from productService.util.mapper import convert_fake_store_category_data_to_category


class FakeStoreCategoryServiceImpl(FakeStoreCategoryService):
    @injector.inject
    def __init__(self):
        self.http_client = httpx.Client
        self.fake_store_category_client = FakeStoreClient()

    def get_all_categories(self) -> List[Category]:
        fake_store_category = self.fake_store_category_client.get_all_categories()
        answer = []
        for category in fake_store_category:
            answer.append(convert_fake_store_category_data_to_category(category_data=category))
        return answer

    def get_in_category(self, category_name) -> List[Category]:
        try:
            category = Category.objects.get(name=category_name)
            products = category.products.all()
            answer = []
            for product in products:
                answer.append(convert_fake_store_category_data_to_category(product))
            return answer
        except Category.DoesNotExist:
            raise ValueError(f"Category with name {category_name} does not exist.")
