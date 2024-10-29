from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView

from userservices.serializer.roleSerializer import RoleSerializer
from userservices.serializer.userSerializer import UserSerializer
from userservices.services.userService import UserService


class UserView(ListCreateAPIView):
    permission_classes = [AllowAny]
    user_service = UserService()

    @csrf_exempt
    def get(self, request, **kwargs):
        users = self.user_service.get_all_users()
        user_id = self.kwargs.get('pk')
        print("user_id :", user_id)
        if user_id:
            user = self.user_service.get_user_details(user_id)
            if not user:
                return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
            serializer = UserSerializer(user)
        else:
            serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @csrf_exempt
    def post(self, request, user_id, **kwargs):
        role_ids = request.data.get('role_ids')
        if not role_ids:
            return Response({"error": "role_ids not provided"}, status=status.HTTP_400_BAD_REQUEST)

        user, roles = self.user_service.set_user_roles(userId=user_id, role_ids=role_ids)

        if user is None:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the user and roles data
        user_serializer = UserSerializer(user)
        roles_serializer = RoleSerializer(roles, many=True)

        response_data = {
            "user": user_serializer.data,
            "roles": roles_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)