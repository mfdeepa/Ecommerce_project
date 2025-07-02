from abc import ABC, abstractmethod
from typing import List

from productservice.models import Category


class FakeStoreCategoryService(ABC):

    @abstractmethod
    def get_all_categories(self) -> List[Category]:
        pass

    @abstractmethod
    def get_in_category(self, category_name) -> List[Category]:
        pass
