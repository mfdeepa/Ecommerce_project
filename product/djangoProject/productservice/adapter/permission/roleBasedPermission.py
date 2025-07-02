from rest_framework.permissions import BasePermission

from productservice.adapter.permission.rolePermissionMapping import RolePermissionMapping
from productservice.adapter.useradapter import UserAdapter


class RoleBasedPermission(BasePermission):
    user_adapter = UserAdapter()

    def has_permission(self, request, view):

        email = request.headers.get('X-User-Email')
        token = request.headers.get('X-Token')

        roles = self.user_adapter.get_role_by_user(email=email, token=token)

        allowed_roles = RolePermissionMapping.get_allowed_roles_for_method(request.method)

        for role in roles:
            if role in allowed_roles:
                return True

        return False

    def has_object_permission(self, request, view, obj):

        return self.has_permission(request, view)
