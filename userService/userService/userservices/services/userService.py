from typing import Optional, List

from django.http import Http404
from injector import Injector, inject

from userservices.manager.roleManager import RoleManager
from userservices.manager.userManager import UserManager
from userservices.models import User, Role
from userservices.serializer.userSerializer import UserSerializer


class UserService:

    @inject
    def __init__(self):
        self.userManager = UserManager()
        self.roleManager = RoleManager()
        self.userSerializer = UserSerializer()

    def get_all_users(self) -> List[User]:
        users = User.objects.all()
        answer = []
        for user in users:
            answer.append(user)
        return answer

    def get_user_details(self, userId) -> Optional[User]:
        try:
            user = User.objects.get(pk=userId)
            return user
        except User.DoesNotExist:
            raise Http404("Product does not exist")

    def set_user_roles(self, userId, role_ids: List[int]):
        user = User.objects.filter(id=userId).first()
        if user is None:
            return None, None

        roles = Role.objects.filter(id__in=role_ids)
        user.roles.set(roles)

        return user, roles
