from rest_framework import serializers


class ValidateTokenRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()
