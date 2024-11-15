from rest_framework import generics, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from productService.adapter.permission.roleBasedPermission import RoleBasedPermission
from productService.models import Product
from productService.seralizers.productSerializer import ProductSerializer
from productService.services.productServiceImpl import ProductServiceImpl


class ProductRetrieveUpdateDestroyAPIView(CreateModelMixin, generics.RetrieveUpdateDestroyAPIView):
    product_ser = ProductServiceImpl()
    permission_classes = [RoleBasedPermission]

    def get(self, request, *args, **kwargs):
        products = self.product_ser.get_all_products()
        product_id = self.kwargs.get('pk')
        print("Product ID: ", product_id)
        if product_id:
            product = self.product_ser.get_single_product(product_id)
            if not product:
                return Response({'error': 'Product not found'}, status=404)
            serializer = ProductSerializer(product).data
        else:
            serializer = ProductSerializer(products, many=True).data
        return Response(serializer, status=200)

    def post(self, request, *args, **kwargs):
        products = self.product_ser.add_new_product(request.data)
        serializer = ProductSerializer(products).data
        return Response(serializer, status=200)

    def put(self, request, *args, **kwargs):
        product_id = self.kwargs.get('pk')
        if not product_id:
            return Response({'error': 'Product not found'}, status=404)
        try:
            product = self.product_ser.update_product(product_id, request.data)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)
        serializer = ProductSerializer(product).data
        return Response(serializer, status=200)

    def delete(self, request, *args, **kwargs):
        product_id = self.kwargs.get('pk')
        if not product_id:
            return Response({'product_id': 'Product id is not found'}, status=404)
        product = self.product_ser.delete_product(product_id)
        print(product)
        if product:
            return Response({'message': 'successful deleted'}, status=404)
        else:
            return Response({'error': 'Product not found'}, status=404)
