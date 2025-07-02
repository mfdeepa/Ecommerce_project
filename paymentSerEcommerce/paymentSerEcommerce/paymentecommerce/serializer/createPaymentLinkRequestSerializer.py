from rest_framework import serializers


class CreatePaymentLinkRequestSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)

