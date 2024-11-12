from datetime import timedelta

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from carts.models import Cart, Product, CartItem, Discount, CartCustomUser
from carts.serializer.cartItemSerializer import CartItemSerializer
from carts.serializer.cartSerializer import CartSerializer


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        # Clean up expired carts
        Cart.objects.filter(expires_at__lt=timezone.now()).delete()

        if self.request.user.is_authenticated:
            return Cart.objects.filter(user=self.request.user)
        return Cart.objects.filter(session_id=self.request.session.session_key)

    @action(detail=False, methods=['get'])
    def get_cart_details(self, request, cart_id=None):
        cart = get_object_or_404(Cart, id=cart_id)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def get_cart(self, cart_id):
        return get_object_or_404(Cart, id=cart_id)

    def get_or_create_cart(self):
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
        else:
            session_id = self.request.session.session_key
            if not session_id:
                self.request.session.create()
                session_id = self.request.session.session_key
            cart, created = Cart.objects.get_or_create(session_id=session_id)

        if cart.is_expired():
            cart.items.all().delete()
            cart.delete()
            return self.get_or_create_cart()
        return cart

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """
        Adds an item to the cart without requiring a cart ID in the request.
        """

        user_id = request.data.get('user_id') if 'user_id' in request.data else request.user.id

        user = get_object_or_404(CartCustomUser, id=user_id)

        cart, created = Cart.objects.get_or_create(user=user)
        print(cart)

        if created:
            print(f"Created a new cart for user {user_id}")

        # cart = self.get_or_create_cart()  # Automatically handle cart retrieval or creation

        with transaction.atomic():
            serializer = CartItemSerializer(data=request.data)
            if serializer.is_valid():
                product = Product.objects.get(pk=serializer.validated_data['product_id'])

                # Check if there is enough inventory
                if not product.check_inventory(serializer.validated_data['quantity']):
                    return Response(
                        {'error': 'Insufficient inventory'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                # Try to get an existing cart item for the same product
                try:
                    cart_item = CartItem.objects.get(cart=cart, product=product)
                    new_quantity = cart_item.quantity + serializer.validated_data['quantity']

                    # Validate new quantity against inventory
                    if not product.check_inventory(new_quantity):
                        return Response(
                            {'error': 'Insufficient inventory for updated quantity'},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    # Update quantity if sufficient inventory is available
                    cart_item.quantity = new_quantity
                    cart_item.save()
                except CartItem.DoesNotExist:
                    # Create a new cart item if it doesn't exist
                    cart_item = CartItem.objects.create(
                        cart=cart,
                        product=product,
                        quantity=serializer.validated_data['quantity'],
                        price=product.price
                    )
                cart_item_serializer = CartItemSerializer(cart_item)
                return Response(cart_item_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], url_path='bulk-add')
    def bulk_add_item(self, request):
        """
        Adds multiple items to the cart at once and returns only the added products.
        Associates the items with the user (user_id).
        """
        # Get the user_id from request data, or use the authenticated user's ID
        user_id = request.data.get('user_id') if 'user_id' in request.data else request.user.id

        # Ensure that the user exists in the database
        user = get_object_or_404(CartCustomUser, id=user_id)

        # Retrieve or create the cart for the user
        cart, created = Cart.objects.get_or_create(user=user)

        # Log creation of a new cart if necessary
        if created:
            print(f"Created a new cart for user {user_id}")

        # Initialize a list to collect responses for each added item
        added_items = []

        with transaction.atomic():
            for item_data in request.data.get('items', []):
                # For each item, validate the data
                serializer = CartItemSerializer(data=item_data)
                if serializer.is_valid():
                    product = Product.objects.get(pk=serializer.validated_data['product_id'])

                    # Check if there is enough inventory
                    if not product.check_inventory(serializer.validated_data['quantity']):
                        return Response(
                            {'error': f'Insufficient inventory for product {product.id}'},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    # Try to get an existing cart item for the same product
                    try:
                        cart_item = CartItem.objects.get(cart=cart, product=product)
                        new_quantity = cart_item.quantity + serializer.validated_data['quantity']

                        # Validate new quantity against inventory
                        if not product.check_inventory(new_quantity):
                            return Response(
                                {'error': f'Insufficient inventory for product {product.id}'},
                                status=status.HTTP_400_BAD_REQUEST
                            )

                        # Update quantity if sufficient inventory is available
                        cart_item.quantity = new_quantity
                        cart_item.save()
                        added_items.append(CartItemSerializer(cart_item).data)

                    except CartItem.DoesNotExist:
                        # Create a new cart item if it doesn't exist, associate it with the user
                        cart_item = CartItem.objects.create(
                            cart=cart,
                            product=product,
                            quantity=serializer.validated_data['quantity'],
                            price=product.price,  # Automatically set the price from Product
                        )
                        added_items.append(CartItemSerializer(cart_item).data)

            # If all items are processed, return the added items
            return Response({'added_items': added_items})

        # If any error occurs during the transaction, return the errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='update-quantity')
    def update_quantity(self, request, cart_id=None):
        """
        Update item quantity in cart
        """
        cart = self.get_cart(cart_id)
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity')

        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        product = cart_item.product

        if not product.check_inventory(quantity):
            return Response(
                {'error': 'Insufficient inventory'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()

        cart = cart_item.cart

        return Response(CartSerializer(cart).data)

    @action(detail=True, methods=['delete'], url_path='delete-item')
    def delete_cart_item(self, request, cart_id=None):
        """
        Decrease quantity of a specific product in the cart.
        If quantity is 0, delete the cart item.
        """
        product_id = request.data.get('product_id')

        if not product_id:
            return Response({'error': 'product_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the cart by id
        cart = get_object_or_404(Cart, id=cart_id)

        # Get the cart item to modify
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

        # If quantity is 0, delete the cart item
        if cart_item.quantity == 0:
            cart_item.delete()
            return Response({'message': 'Item successfully removed from cart because quantity is 0'},
                            status=status.HTTP_204_NO_CONTENT)

        # If quantity > 0, decrease it by 1
        if cart_item.quantity > 0:
            cart_item.quantity -= 1
            cart_item.save()
            return Response({'message': 'Item quantity decreased by 1', 'new_quantity': cart_item.quantity},
                            status=status.HTTP_200_OK)

        return Response({'error': 'Quantity cannot be less than 0'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], url_path='clear-cart')
    def clear_cart(self, request, cart_id=None):
        """
        Clear all items from the cart.
        """
        # Get the cart by id
        cart = get_object_or_404(Cart, id=cart_id)

        # Delete all CartItems associated with the cart
        cart_items = CartItem.objects.filter(cart=cart)
        deleted_count, _ = cart_items.delete()  # delete and return number of deleted items

        if deleted_count > 0:
            return Response({
                'message': f'{deleted_count} items successfully removed from the cart.'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'No items found in the cart to remove.'
            }, status=status.HTTP_400_BAD_REQUEST)
