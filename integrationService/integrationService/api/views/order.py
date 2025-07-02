from rest_framework.views import APIView
from rest_framework.response import Response
from api.services.user_service import validate_token
from api.services.cart_service import get_user_cart
from api.services.order_service import place_order

class PlaceOrderView(APIView):
    def post(self, request):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        try:
            user = validate_token(token)
            user_id = user.get("id") or user.get("user_id")

            cart = get_user_cart(token)

            if not cart.get("items"):
                return Response({"detail": "Cart is empty"}, status=400)

            shipping_address = request.data.get("shipping_address")
            billing_address = request.data.get("billing_address", shipping_address)
            payment_method = request.data.get("payment_method")

            order = place_order(user_id, token, cart, shipping_address, billing_address, payment_method)

            return Response(order, status=201)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"detail": str(e)}, status=400)
