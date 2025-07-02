from django.http import Http404
from rest_framework import generics, viewsets
from rest_framework.exceptions import PermissionDenied, ValidationError, AuthenticationFailed
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from productservice.models import Product
from productservice.seralizers.productSerializer import ProductSerializer
from productservice.services.productServiceImpl import ProductServiceImpl


class ProductRetrieveUpdateDestroyAPIView(CreateModelMixin, generics.RetrieveUpdateDestroyAPIView):
    product_ser = ProductServiceImpl()

    def get_permissions(self):
        return [AllowAny()]

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
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise AuthenticationFailed("Invalid or missing Authorization header.")

        token = auth_header.split(" ")[1]
        user_data = self.product_ser.validate_user_from_token(token)

        roles = user_data.get("roles", [])
        if "customer" in [role.lower() for role in roles]:
            raise PermissionDenied("Customers are not allowed to create products.")

        product = self.product_ser.add_new_product(request.data, token)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=201)

    def put(self, request, *args, **kwargs):
        print("PUT method with URL param called")

        product_id = self.kwargs.get("pk")

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise AuthenticationFailed("Invalid or missing Authorization header.")

        token = auth_header.replace("Bearer ", "").strip()

        user_data = self.product_ser.validate_user_from_token(token)
        roles = user_data.get("roles", [])

        if "customer" in [role.lower() for role in roles]:
            raise PermissionDenied("Customers are not allowed to update products.")

        try:
            product = self.product_ser.update_product(product_id, request.data, token)
        except Http404:
            return Response({"detail": "Product not found"}, status=404)

        serializer = ProductSerializer(product)
        return Response(serializer.data, status=200)

    def delete(self, request, *args, **kwargs):
        product_id = self.kwargs.get("pk")
        if not product_id:
            return Response({"detail": "Product ID is required in the URL"}, status=400)

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise AuthenticationFailed("Invalid or missing Authorization header.")

        token = auth_header.replace("Bearer ", "").strip()

        try:
            self.product_ser.delete_product(product_id, token)
        except Http404:
            return Response({"detail": "Product not found"}, status=404)
        except PermissionDenied as e:
            return Response({"detail": str(e)}, status=403)

        return Response({"detail": "Product deleted successfully."}, status=204)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
