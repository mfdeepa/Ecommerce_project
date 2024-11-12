from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from carts.models import Product
from carts.serializer.productSerializer import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # @action(detail=True, methods=['get'])         for this method,first, we have to call product id and then check-inventory so url will be according to this.
    # def check_inventory(self, request, pk=None):
    #     try:
    #         # Retrieve the product using pk
    #         product = Product.objects.get(pk=pk)
    #         return Response({
    #             'product_id': product.id,
    #             'inventory_count': product.inventory_count,
    #             'available': product.inventory_count > 0
    #         })
    #     except Product.DoesNotExist:
    #         return Response({'error': 'Product not found'}, status=404)

    @action(detail=True, methods=['get'])
    def check_inventory(self, request, product_id):
        # Retrieve the product using the product_id parameter
        product = get_object_or_404(Product, pk=product_id)
        return Response({
            'product_id': product.id,
            'inventory_count': product.inventory_count,
            'available': product.inventory_count > 0
        })
