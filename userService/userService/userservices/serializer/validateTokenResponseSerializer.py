import injector
from rest_framework import serializers

from userservices.serializer.userSerializer import UserSerializer
from userservices.sessionStatus import SessionStatus


class ValidateTokenResponseSerializer(serializers.Serializer):
    @injector.Inject
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.UserSerializer = UserSerializer()
        self.SessionStatus = SessionStatus.value
