from rest_framework import serializers


class SetUserRolesRequestSerializer(serializers.Serializer):
    role_ids = serializers.ListField(child=serializers.IntegerField())
    