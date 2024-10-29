from rest_framework import serializers


class LogoutRequestSerializer(serializers.Serializer):
    token = serializers.CharField()
    # email = serializers.EmailField(required=True)
    user_id = serializers.IntegerField()   #if we want to logout through userid then we have to uncomment this filed.
