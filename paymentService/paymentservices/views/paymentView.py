import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from stripe import Webhook

from paymentService import settings
from paymentservices.serializer.createPaymentLinkResponseSerializer import CreatePaymentLinkResponseSerializer
from paymentservices.serializer.createPaymentLinkrequestSerializer import CreatePaymentLinkRequestSerializer
from paymentservices.service.paymentService import PaymentService


class PaymentServiceView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.payment_service = PaymentService()

    def post(self, request):
        serializer = CreatePaymentLinkRequestSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            order_id = serializer.validated_data['order_id']
            print("order id is :", order_id)

            try:
                # Use the payment service to create the payment link
                url = self.payment_service.create_payment_link(order_id)
                print("url is :", url)

                # Serialize the response
                response_serializer = CreatePaymentLinkResponseSerializer(data={'url': url})
                print(response_serializer)
                if response_serializer.is_valid():
                    return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentServiceWebhookView(APIView):
    webhook_secret_key = settings.STRIPE_WEBHOOK_SECRET_KEY

    def post(self, request):
        webhook = Webhook()
        webhook.construct_event()

    pass


class StripeWebhookView(APIView):
    @csrf_exempt
    def post(self, request):
        payload = request.body
        sig_header = request.headers.get('Stripe-Signature')
        endpoint_secret = settings.STRIPE_WEBHOOK_SECRET_KEY  # Ensure this is set in your settings

        try:
            # Verify webhook event
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            return JsonResponse({"error": "Invalid payload"}, status=400)
        except stripe.error.SignatureVerificationError as e:
            return JsonResponse({"error": "Invalid signature"}, status=400)

        # Process the specific events you’re interested in
        if event['type'] == 'payment_link.completed':
            payment_data = event['data']['object']
            # Handle post-payment logic here, like updating the order status
            print("Payment completed:", payment_data)
            # You could also trigger any custom business logic, such as sending confirmation emails.

        return JsonResponse({"status": "success"}, status=200)
