from decimal import Decimal

from rest_framework.views import APIView
from rest_framework.response import Response

from api.services.order_service import get_user_order
from api.services.payment_service import create_payment
from api.services.user_service import validate_token


class PaymentInitiateView(APIView):
    def post(self, request):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        try:
            user = validate_token(token)
            user_id = user.get("id") or user.get("user_id")
            user_name = user.get("username")
            user_email = user.get("email")
            user_mobile = user.get("phone_number")

            order_response = get_user_order(token)
            order_list = order_response.get("orders", [])

            if not order_list:
                return Response({"detail": "order is empty"}, status=400)

            else:
                total_amount = Decimal("0.00")
                order_id = None

                # Loop over each response in the list
                for order in order_list:
                    # Sum total_amount
                    total_amount += Decimal(order["total_amount"])

                    # Track max order ID
                    if order_id is None or order["id"] > order_id:
                        order_id = order["id"]

            payment = create_payment(order_id, token, user_name, user_email, user_mobile, total_amount)

            return Response(payment, status=201)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({"detail": str(e)}, status=400)
