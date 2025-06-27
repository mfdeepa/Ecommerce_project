import string
from datetime import timedelta
from random import choices

from django.utils import timezone
from injector import inject
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password, make_password

from userservices.exceptions.userDoesNotExistException import UserDoesNotExistException
from userservices.manager.sessionManager import SessionManager
from userservices.manager.userManager import UserManager
from userservices.models import User, Session, Role
from userservices.serializer.userSerializer import UserSerializer
from userservices.sessionStatus import SessionStatus
from userservices.utils import generate_code_verifier_and_challenge

code_verifier, code_challenge = generate_code_verifier_and_challenge()


class AuthService:

    @inject
    def __init__(self):
        self.user_manager = UserManager()
        self.session_manager = SessionManager()

    def login(self, email: str, password: str):
        user = User.objects.filter(email=email).prefetch_related('roles').first()
        if user:
            print(f"Roles for {user.email}: {user.roles.all()}")
        if not user:
            raise UserDoesNotExistException(f"User with email: {email}, doesn't exist.")

        if not check_password(password, user.password):
            print(password)
            print(user.password)
            return None

        refresh_token = RefreshToken.for_user(user)                     # generated jwt token
        # token = ''.join(choices(string.ascii_letters + string.digits, k=20))  #generated random token

        try:
            session = Session.objects.create(
                user=user,                              # Ensure this is a User instance
                token=refresh_token,
                session_status="Active",
                expiring_at=timezone.now() + timedelta(hours=1)
            )
        except Exception as e:
            print(f"Session creation failed: {e}")
            return None
        user_data = UserSerializer(user).data
        print("user data", user_data)
        return user_data, refresh_token

    def signup(self, email: str, password: str, role) -> User:
        user = User.objects.filter(email=email).first()
        if user is not None:
            raise UserDoesNotExistException(f"User with email: {email}, already exist.")

        user = User(email=email, password=make_password(password))

        user.save()
        role_instance = Role.objects.get(name=role)
        user.roles.add(role_instance)

        user.save()

        return user

    """"
    # def logout(self, token: str, email: str):     # use when we want to logout via email.
    #     user = User.objects.filter(email=email).first()
    #     if not user:
    #         return None
    #     session_optional = Session.objects.filter(token=token, user=user).first()
    #     if session_optional is None:
    #         return None
    # 
    #     session_optional.session_status = "Logged out"
    #     session_optional.save()
    #     return session_optional
    """

    """  if we want to logout through user_id then use it. """
    def logout(self, token: str, user_id: str):
        session_optional = Session.objects.filter(token=token, user_id=user_id).first()
        if session_optional is None:
            return None

        session_optional.session_status = "Logged out"
        session_optional.save()
        return session_optional

    def validate(self, token: str, email: str):
        session_optional = Session.objects.filter(token=token, user__email=email).first()

        if session_optional is None:
            return None
        print(session_optional.session_status)
        if session_optional.session_status != SessionStatus.Active.value:
            print("session is not active")
            return None

        # user = User.objects.get(id=email)
        user = session_optional.user
        print(user)
        userSerializer = UserSerializer(instance=user)
        return userSerializer

    """" this below validate method is used for validate token with user_id

    # def validate(self, token: str, user_id: str):
    #     session_optional = Session.objects.filter(token=token, user_id=user_id).first()
    #
    #     if session_optional is None:
    #         return None
    #     print(session_optional.session_status)
    #     if session_optional.session_status != SessionStatus.Active.Active.value:
    #         print("session is not active")
    #         return None
    #
    #     user = User.objects.get(id=user_id)
    #     print(user)
    #     userSerializer = UserSerializer(instance=user)
    #     return userSerializer

    """