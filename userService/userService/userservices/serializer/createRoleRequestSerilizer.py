from rest_framework import serializers


class CreateRoleRequestSerializer(serializers.Serializer):
    name = serializers.CharField()