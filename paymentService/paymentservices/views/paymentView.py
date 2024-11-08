from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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
