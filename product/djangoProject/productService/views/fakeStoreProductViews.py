from rest_framework import generics, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from productService.models import Product
from productService.seralizers.productSerializer import ProductSerializer
from productService.services.fakeStoreProductServiceImpl import FakeStoreProductServiceImpl


class FakeStoreProductRetrieveUpdateDestroyAPIView(CreateModelMixin, generics.RetrieveUpdateDestroyAPIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.product_ser = FakeStoreProductServiceImpl()

    def get(self, request, *args, **kwargs):
        products = self.product_ser.get_all_products()
        product_id = self.kwargs.get('product_id')
        print("product_id", product_id)
        if product_id:
            product = self.product_ser.get_single_product(product_id)
            if not product:
                return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
            serialized_product = ProductSerializer(product).data
            return Response(serialized_product)
        else:
            serialized_products = ProductSerializer(products, many=True).data
        return Response(serialized_products)

    def post(self, request, *args, **kwargs):
        products = self.product_ser.add_new_product(request.data)
        serialized_products = ProductSerializer(products, many=False).data
        return Response(serialized_products)

    def patch(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        print(product_id)
        if not product_id:
            return Response({"detail": "product not found."}, status=404)
        try:
            product = self.product_ser.update_product(product_id, request.data)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found."}, status=404)
        serialized_product = ProductSerializer(product, many=False).data
        return Response(serialized_product)

    def delete(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        delete_products = self.product_ser.delete_product(product_id)
        if delete_products:
            return Response("Product deleted successfully.")
        elif isinstance(delete_products, Product):
            # If you want to return the deleted product data, ensure the product object is serialized
            serialized_product = ProductSerializer(delete_products).data
            return Response(serialized_product, status=200)
        else:
            return Response({"error": "Product not found or could not be deleted."}, status=404)


