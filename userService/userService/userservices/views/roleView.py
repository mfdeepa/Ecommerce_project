from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from userservices.exceptions.roleAlreadyExitsException import RoleAlreadyExitsException
from userservices.serializer.createRoleRequestSerilizer import CreateRoleRequestSerializer
from userservices.services.roleService import RolesService


class RoleViewSet(CreateAPIView):
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.role_service = RolesService()

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        serializer = CreateRoleRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            role = self.role_service.create_role(serializer.validated_data['name'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except RoleAlreadyExitsException:
            return Response({"error": "Role already exists"}, status=status.HTTP_409_CONFLICT)
