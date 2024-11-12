from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from decimal import Decimal
from carts.models import Cart, Discount, CartItem
from carts.view.cartView import CartViewSet


class CartDiscountViewSet(viewsets.ModelViewSet):
    cart_view = CartViewSet()
    # ... existing code ...

    @action(detail=True, methods=['post'], url_path='apply-discount')
    def apply_discount(self, request, cart_id=None):
        """
        Apply discount to a specific product in the cart based on:
        - Fixed discount
        - Percentage discount
        - Coupon code discount
        - Defaults to 0 if no discount is applied
        """
        cart = self.cart_view.get_cart(cart_id)  # Retrieve the cart by ID
        product_id = request.data.get('product_id')
        discount_code = request.data.get('discount_code')
        fixed_discount_amount = request.data.get('fixed_discount_amount', Decimal('0.00'))
        percentage_discount = request.data.get('percentage_discount', 0)

        # Retrieve the product's CartItem from the cart
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        original_price = cart_item.get_subtotal()  # Total price of the product in cart

        # Initialize discount amount
        discount_amount = Decimal('0.00')

        # 1. Apply fixed discount if provided
        if fixed_discount_amount:
            discount_amount += min(fixed_discount_amount, original_price)

        # 2. Apply percentage discount if provided
        if percentage_discount > 0:
            discount_amount += (original_price * Decimal(percentage_discount)) / 100

        # 3. Apply additional discount if a valid coupon code is provided
        if discount_code:
            try:
                discount = Discount.objects.get(code=discount_code)
                if discount.is_valid(original_price):
                    # Check discount type for coupon and apply accordingly
                    if discount.discount_type == 'percentage':
                        discount_amount += (original_price * discount.value) / 100
                    elif discount.discount_type == 'fixed':
                        discount_amount += min(discount.value, original_price)
            except Discount.DoesNotExist:
                return Response({'error': 'Invalid discount code'}, status=status.HTTP_400_BAD_REQUEST)

        # 4. Ensure discount does not exceed the original price
        discounted_price = max(original_price - discount_amount, Decimal('0.00'))

        # Optional: Update CartItem with discounted price (assuming a `discounted_price` field exists)
        cart_item.discounted_price = discounted_price
        cart_item.save()

        return Response({
            'product_id': product_id,
            'original_price': str(original_price),
            'fixed_discount': str(fixed_discount_amount),
            'percentage_discount': str(percentage_discount),
            'coupon_discount': str(
                discount_amount - fixed_discount_amount - (original_price * Decimal(percentage_discount) / 100)),
            'total_discount': str(discount_amount),
            'discounted_price': str(discounted_price)
        }, status=status.HTTP_200_OK)
