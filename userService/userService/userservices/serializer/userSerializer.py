from rest_framework import serializers

from userservices.models import Role, User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    roles = serializers.SlugRelatedField(  # represent data into a list
        many=True,
        slug_field='name',
        queryset=Role.objects.all(),
        required=False
    )

    class Meta:
        model = User
        fields = ['email', 'roles', 'password']
        extra_kwargs = {
            'password': {'write_only': True}  # Don't send password in responses
        }

    def create(self, validated_data):
        roles_data = validated_data.pop('roles', [])
        user = User.objects.create(**validated_data)
        user.roles.set(roles_data)
        return user

    def get_roles(self, obj):
        try:
            # Get role names directly
            return list(obj.roles.values_list('name', flat=True))
        except Exception as e:
            print(f"Error getting roles: {e}")
            return []

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if hasattr(instance, 'roles'):
            representation['roles'] = [role.name for role in instance.roles.all()]
        return representation
