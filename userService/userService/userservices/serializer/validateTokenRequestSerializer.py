from rest_framework import serializers


class ValidateTokenRequestSerializer(serializers.Serializer):
    # user_id = serializers.IntegerField()
    email = serializers.EmailField()
    token = serializers.CharField()
