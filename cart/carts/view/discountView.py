from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.shortcuts import get_object_or_404
from decimal import Decimal

from carts.models import Cart, Discount, CartItem
from carts.services.cart_service import get_or_create_cart
from carts.services.user_validation import UserAuthValidator


class CartDiscountViewSet(viewsets.ViewSet):
    def get_user_id_from_token(self, request):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        user_data = UserAuthValidator.validate_token(token)
        return user_data.get("user_id")

    @action(detail=False, methods=['post'], url_path='apply-discount')
    def apply_discount(self, request):

        user_id = self.get_user_id_from_token(request)
        cart = get_or_create_cart(user_id=user_id)

        product_id = request.data.get('product_id')
        if not product_id:
            return Response({"error": "product_id is required"}, status=400)

        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
        original_price = cart_item.get_subtotal()

        fixed_discount_amount = Decimal(request.data.get('fixed_discount_amount', '0.00'))
        fixed_discount_value = min(fixed_discount_amount, original_price)

        try:
            percentage_discount = Decimal(request.data.get('percentage_discount', '0.00'))
        except:
            percentage_discount = Decimal('0.00')

        percentage_discount_value = (original_price * percentage_discount) / 100 if percentage_discount > 0 else Decimal('0.00')

        discount_code = request.data.get('discount_code')
        coupon_discount_value = Decimal('0.00')

        if discount_code:
            try:
                discount = Discount.objects.get(code=discount_code)
                if discount.is_valid(original_price):
                    coupon_discount_value = discount.calculate_discount(original_price)
                else:
                    return Response({'error': 'Discount code is not valid for this cart total or time window.'}, status=400)
            except Discount.DoesNotExist:
                return Response({'error': 'Invalid discount code'}, status=400)

        total_discount = fixed_discount_value + percentage_discount_value + coupon_discount_value
        final_price = max(original_price - total_discount, Decimal('0.00'))

        return Response({
            "product_id": product_id,
            "original_price": str(original_price),
            "fixed_discount": str(fixed_discount_value),
            "percentage_discount": str(percentage_discount_value),
            "coupon_discount": str(coupon_discount_value),
            "total_discount": str(total_discount),
            "final_price": str(final_price)
        }, status=200)
