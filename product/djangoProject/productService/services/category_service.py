from abc import ABC, abstractmethod

from productService.seralizers.categorySerializer import CategorySerializer


class CategoryService(ABC):
    @abstractmethod
    def get_category(self, category_id):
        pass

    @abstractmethod
    def create_category(self, category_request_serializer: CategorySerializer):
        pass

    @abstractmethod
    def update_category(self, category_id: int, category_name):
        pass

    @abstractmethod
    def delete_category(self, category_request_serializer: CategorySerializer) -> bool:
        pass

    # @abstractmethod
    # def get_product_in_category(self) -> str:
    #     pass
