import traceback

import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from stripe import Webhook

from paymentSerEcommerce import settings
from paymentecommerce.serializer.createPaymentLinkRequestSerializer import CreatePaymentLinkRequestSerializer
from paymentecommerce.serializer.createPaymentLinkResponseSerializer import CreatePaymentLinkResponseSerializer
from paymentecommerce.services.paymentService import PaymentService
from paymentecommerce.services.user_validation import UserAuthValidator


def authenticate_user(request):
    """
    Extract and validate user token from request headers
    """
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise AuthenticationFailed("Authorization header is required.")

    if not auth_header.startswith('Bearer '):
        raise AuthenticationFailed("Invalid authorization header format. Use 'Bearer <token>'.")

    token = auth_header.split(' ')[1]
    user_data = UserAuthValidator.validate_token(token)
    return user_data


class PaymentServiceView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.payment_service = PaymentService()

    def post(self, request):

        try:
            user_data = authenticate_user(request)
            user_id = user_data.get("user_id")
            user_name = user_data.get("user_name") or user_data.get("username")
            user_email = user_data.get("email")
            user_mobile = user_data.get("phone_number") or user_data.get("phone")

        except AuthenticationFailed as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CreatePaymentLinkRequestSerializer(data=request.data)
        if serializer.is_valid():
            order_id = serializer.validated_data['order_id']
            total_amount = serializer.validated_data['total_amount']

            try:
                url = self.payment_service.create_payment_link(order_id=order_id, total_amount=total_amount,
                                                               user_name=user_name, user_mobile=user_mobile,
                                                               user_email=user_email)

                response_serializer = CreatePaymentLinkResponseSerializer(data={'url': url})
                if response_serializer.is_valid():
                    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(response_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentServiceWebhookView(APIView):
    webhook_secret_key = settings.STRIPE_WEBHOOK_SECRET_KEY

    def post(self, request):
        webhook = Webhook()
        webhook.construct_event()


class StripeWebhookView(APIView):
    @csrf_exempt
    def post(self, request):
        payload = request.body
        sig_header = request.headers.get('Stripe-Signature')
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET_KEY

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            return JsonResponse({"error": "Invalid payload"}, status=400)
        except stripe.error.SignatureVerificationError as e:
            return JsonResponse({"error": "Invalid signature"}, status=400)

        if event['type'] == 'payment_link.completed':
            payment_data = event['data']['object']
            print("Payment completed:", payment_data)

        return JsonResponse({"status": "success"}, status=200)
