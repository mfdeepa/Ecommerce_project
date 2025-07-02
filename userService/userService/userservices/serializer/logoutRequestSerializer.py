from rest_framework import serializers


class LogoutRequestSerializer(serializers.Serializer):
    token = serializers.CharField()
    email = serializers.EmailField(required=False)
    user_id = serializers.IntegerField()
