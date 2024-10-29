from abc import ABC, abstractmethod
from typing import List, Optional

from productService.models import Product
from productService.seralizers.productSerializer import ProductSerializer


class ProductService(ABC):

    @abstractmethod
    def get_all_products(self) -> List[Product]:
        pass

    @abstractmethod
    def get_single_product(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def add_new_product(self, product: ProductSerializer) -> Product:
        pass

    @abstractmethod
    def update_product(self, product_id: int, product: Product) -> Product:
        pass

    @abstractmethod
    def delete_product(self, product_id: int) -> bool:
        pass

    @abstractmethod
    def get_limit_product_result(self, limit: int, offset: int) -> str:
        pass

    @abstractmethod
    def update_product_partially(self, product_id: int) -> str:
        pass

    @abstractmethod
    def get_product_by_sorting(self, product_id: int) -> str:
        pass
