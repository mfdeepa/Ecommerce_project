from abc import ABC, abstractmethod
from typing import List

import httpx
import injector

from productService.clients.fakeStoreClient.fakeStoreClient import FakeStoreClient
from productService.models import Category
from productService.util.mapper import convert_fake_store_category_data_to_category


class FakeStoreCategoryService(ABC):

    @abstractmethod
    def get_all_categories(self) -> List[Category]:
        pass

    @abstractmethod
    def get_in_category(self, category_name) -> List[Category]:
        pass
