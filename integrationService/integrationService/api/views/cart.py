from rest_framework.views import APIView
from rest_framework.response import Response

from api.services.cart_service import add_to_cart
from api.services.product_service import get_product
from api.services.user_service import validate_token


class AddToCartView(APIView):

    def post(self, request):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        try:
            user = validate_token(token)

            user_id = user.get("id") or user.get("user_id")
            if not user_id:
                raise Exception("User ID missing in token validation response.")

            product_id = request.data.get("product_id")
            quantity = request.data.get("quantity", 1)

            product = get_product(product_id, token)

            if product.get("quantity", 0) < quantity:
                return Response({"detail": "Insufficient product quantity"}, status=400)

            cart = add_to_cart(user_id, product_id, quantity, token)
            return Response(cart, status=201)

        except Exception as e:
            return Response({"detail": str(e)}, status=400)
