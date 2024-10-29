from rest_framework import serializers


class ValidateTokenRequestSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    token = serializers.CharField()
