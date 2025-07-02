from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from carts.models import Cart, Product, CartItem
from carts.serializer.cartItemSerializer import CartItemSerializer
from carts.serializer.cartSerializer import CartSerializer

from carts.services.cart_service import delete_cart_item, update_cart_item_quantity, get_or_create_cart, \
    add_item_to_cart
from carts.services.user_validation import UserAuthValidator


class CartViewSet(viewsets.ViewSet):
    def get_user_id_from_token(self, request):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        user_data = UserAuthValidator.validate_token(token)
        return user_data.get("user_id")

    def get_cart(self, user_id):
        return get_or_create_cart(user_id=user_id)

    @action(detail=False, methods=["get"])
    def cart(self, request):
        user_id = self.get_user_id_from_token(request)
        cart = self.get_cart(user_id)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def add_item(self, request):
        user_id = self.get_user_id_from_token(request)
        cart = self.get_cart(user_id)

        items_data = request.data.get("items", [])

        if not items_data:
            return Response({"error": "No items provided."}, status=400)

        added_items = []
        for item in items_data:
            serializer = CartItemSerializer(data=item)
            if serializer.is_valid():
                validated = serializer.validated_data
                with transaction.atomic():
                    cart_item = CartItem.objects.create(
                        cart=cart,
                        product_id=validated["product_id"],
                        title=validated["title"],
                        price=validated["price"],
                        quantity=validated["quantity"]
                    )
                    added_items.append(CartItemSerializer(cart_item).data)
            else:
                return Response(serializer.errors, status=400)

        return Response({"added_items": added_items}, status=201)

    @action(detail=True, methods=["post"])
    def update_quantity(self, request, pk=None):
        user_id = self.get_user_id_from_token(request)
        product_id = request.data.get("product_id")
        quantity = request.data.get("quantity")

        cart = self.get_cart(user_id)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

        updated_item = update_cart_item_quantity(cart_item.id, quantity)
        if updated_item:
            return Response(CartItemSerializer(updated_item).data)
        return Response({"message": "Item deleted"}, status=204)

    @action(detail=True, methods=["delete"])
    def delete_item(self, request, pk=None):
        user_id = self.get_user_id_from_token(request)
        product_id = request.data.get("product_id")

        cart = self.get_cart(user_id)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

        delete_cart_item(cart_item.id)
        return Response({"message": "Item deleted"}, status=204)

    @action(detail=False, methods=["post"])
    def clear_cart(self, request):
        user_id = self.get_user_id_from_token(request)
        cart = self.get_cart(user_id)
        deleted, _ = CartItem.objects.filter(cart=cart).delete()
        return Response({"message": f"{deleted} items removed."}, status=200)
