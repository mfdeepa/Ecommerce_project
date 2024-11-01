from django.views.decorators.csrf import csrf_exempt
from injector import inject
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from userservices.exceptions.userAlreadyExitsException import UserAlreadyExitsException
from userservices.serializer.loginRequestSerializer import LoginRequestSerializer
from userservices.serializer.logoutRequestSerializer import LogoutRequestSerializer
from userservices.serializer.signUpRequestSerializer import SignUpRequestSerializer
from userservices.serializer.userSerializer import UserSerializer
from userservices.serializer.validateTokenRequestSerializer import ValidateTokenRequestSerializer
from userservices.services.authService import AuthService
from rest_framework.permissions import IsAuthenticated


class AuthView(APIView):
    auth_service = AuthService()
    permission_classes = [AllowAny]

    @csrf_exempt
    def post(self, request):
        if 'login' in request.path:
            serializer = LoginRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            login_result = self.auth_service.login(serializer.validated_data['email'],
                                                   serializer.validated_data['password'])
            print(login_result)
            if login_result is None:
                return Response({"error": "Wrong password or failed to create session."},
                                status=status.HTTP_404_NOT_FOUND)

            user, refresh_token = login_result
            user_serializer = UserSerializer(user)  # Ensure to serialize the user instance

            response_data = {
                'user': user_serializer.data,  # Use .data to get serialized data
                'refresh': str(refresh_token),
                'access': str(refresh_token.access_token),
            }

            return Response(response_data, status=status.HTTP_200_OK)

        elif 'logout' in request.path:
            serializer = LogoutRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.auth_service.logout(serializer.validated_data['token'], serializer.validated_data['email'])
            return Response(status=status.HTTP_200_OK)

        elif 'signup' in request.path:
            serializer = SignUpRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                user = self.auth_service.signup(serializer.validated_data['email'],
                                                serializer.validated_data['password'])
                return Response(UserSerializer(user).data,
                                status=status.HTTP_201_CREATED)  # Response with serialized user data
            except UserAlreadyExitsException:
                return Response({"error": "User already exists"}, status=status.HTTP_409_CONFLICT)

        elif 'validate' in request.path:
            serializer = ValidateTokenRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = self.auth_service.validate(serializer.validated_data['token'], serializer.validated_data['user_id'])
            if user is None:
                response_data = {"session_status": "INVALID"}
            else:
                response_data = {
                    "session_status": "ACTIVE",
                    "user": user.data
                }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)