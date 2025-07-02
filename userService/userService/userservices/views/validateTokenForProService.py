from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
import jwt
from django.conf import settings


@api_view(['GET'])
@permission_classes([AllowAny])
@authentication_classes([])  # Disable DRF's auth requirement for this endpoint
def validate_token(request):

    token = request.query_params.get("token")
    if not token:
        return Response({"detail": "Token not provided"}, status=400)

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
        User = get_user_model()
        all_users = list(User.objects.all().values("id", "email", "username","phone_number"))

        user = User.objects.filter(id=user_id).first()

        if not user:
            return Response({
                "detail": "User not found",
                "user_id": user_id,
                "debug_users": all_users
            }, status=404)

        roles = []
        if hasattr(user, 'roles'):
            roles = list(user.roles.values_list("name", flat=True))

        return Response({
            "user_id": user.id,
            "email": user.email,
            "username": user.username,
            "phone_number": user.phone_number,
            "roles": roles
        })

    except jwt.ExpiredSignatureError:
        return Response({"detail": "Token has expired"}, status=401)
    except jwt.DecodeError:
        return Response({"detail": "Token is invalid"}, status=401)
    except Exception as e:
        print("🔥 Unexpected error:", str(e))
        return Response({"detail": "Unexpected error", "error": str(e)}, status=500)


