from rest_framework import serializers

from userservices.models import Role, User


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    roles = serializers.SlugRelatedField(  # represent data into a list
        many=True,
        slug_field='role',
        queryset=Role.objects.all()
    )

    class Meta:
        model = User
        fields = ['email', 'roles', 'password']

    def to_representation(self, instance):
        # Get the default representation
        representation = super().to_representation(instance)

        # Convert roles to a set for unique values
        representation['roles'] = list(set(representation['roles']))

        return representation
