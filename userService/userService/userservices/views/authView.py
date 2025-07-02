from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
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
import logging


class AuthView(APIView):
    auth_service = AuthService()
    # permission_classes = [AllowAny]
    # permission_classes = [IsAuthenticated, TokenHasReadWriteScope]
    logger = logging.getLogger(__name__)

    def get_permissions(self):

        if 'validate' in self.request.path:
            return [AllowAny()]
        return [IsAuthenticated(), TokenHasReadWriteScope()]

    @csrf_exempt
    def post(self, request):
        if 'login' in request.path:
            try:
                self.logger.debug(f"Login attempt for: {request.data.get('email')}")
                serializer = LoginRequestSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)

                login_result = self.auth_service.login(
                    serializer.validated_data['email'],
                    serializer.validated_data['password']
                )

                if login_result is None:
                    return Response(
                        {"error": "Wrong password or failed to create session."},
                        status=status.HTTP_404_NOT_FOUND
                    )

                user, refresh_token = login_result

                response_data = {
                    'user': {
                        'email': user['email'],
                        'roles': user['roles']
                    },
                    'refresh': str(refresh_token),
                    'access': str(refresh_token.access_token),
                }

                return Response(response_data, status=status.HTTP_200_OK)

            except Exception as e:
                self.logger.error(f"Login error: {str(e)}")
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        elif 'logout' in request.path:
            serializer = LogoutRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.auth_service.logout(serializer.validated_data['token'], serializer.validated_data['user_id'])

            return Response(status=status.HTTP_200_OK)

        elif 'signup' in request.path:
            serializer = SignUpRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            try:
                user = self.auth_service.signup(serializer.validated_data['email'],
                                                serializer.validated_data['password'],
                                                serializer.validated_data['role'])
                return Response(UserSerializer(user).data,
                                status=status.HTTP_201_CREATED)  # Response with serialized user data
            except UserAlreadyExitsException:
                return Response({"error": "User already exists"}, status=status.HTTP_409_CONFLICT)

        elif 'validate' in request.path:
            serializer = ValidateTokenRequestSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = self.auth_service.validate(serializer.validated_data['token'], serializer.validated_data['email'])
            if user is None:
                response_data = {"session_status": "INVALID"}
            else:
                response_data = {
                    "session_status": "ACTIVE",
                    "user": user.data
                }
            return Response(response_data, status=status.HTTP_200_OK)

        return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)


# this is added for checking the access token instead of refresh token in product service
# class ValidateTokenView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         user = request.user
#         return Response({
#             "id": user.id,
#             "email": user.email,
#             "roles": list(user.roles.values_list('role', flat=True))
#         }, status=200)
#
