from abc import ABC, abstractmethod

from productservice.seralizers.categorySerializer import CategorySerializer


class CategoryService(ABC):
    @abstractmethod
    def get_category(self, category_id):
        pass

    @abstractmethod
    def create_category(self, category_request_serializer: CategorySerializer, token: str):
        pass

    @abstractmethod
    def update_category(self, category_id: int, category_name, token: str):
        pass

    @abstractmethod
    def delete_category(self, category_request_serializer: CategorySerializer, token: str) -> bool:
        pass
