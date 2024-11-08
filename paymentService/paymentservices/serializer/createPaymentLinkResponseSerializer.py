from rest_framework import serializers


class CreatePaymentLinkResponseSerializer(serializers.Serializer):
    url = serializers.CharField()
