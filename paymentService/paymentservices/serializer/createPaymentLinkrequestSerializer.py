from rest_framework import serializers


class CreatePaymentLinkRequestSerializer(serializers.Serializer):
    # amount = serializers.IntegerField()
    order_id = serializers.IntegerField()
    # name = serializers.CharField()
    # contact = serializers.CharField()
    # email = serializers.EmailField()
    # description = serializers.CharField()
