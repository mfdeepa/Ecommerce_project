from abc import ABC, abstractmethod
from typing import List, Optional

from productservice.models import Product
from productservice.seralizers.productSerializer import ProductSerializer

class ProductService(ABC):

    @abstractmethod
    def get_all_products(self) -> List[Product]:
        pass

    @abstractmethod
    def get_single_product(self, product_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def add_new_product(self, product: ProductSerializer, token: str) -> Product:
        pass

    @abstractmethod
    def update_product(self, product_id: int, product: Product, token: str) -> Product:
        pass

    @abstractmethod
    def delete_product(self, product_id: int, token: str) -> bool:
        pass


