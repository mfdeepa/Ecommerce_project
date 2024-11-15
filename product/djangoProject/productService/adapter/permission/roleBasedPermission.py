from rest_framework.permissions import BasePermission

from productService.adapter.permission.rolePermissionMapping import RolePermissionMapping
from productService.adapter.useradapter import UserAdapter


class RoleBasedPermission(BasePermission):
    user_adapter = UserAdapter()

    """
    Custom permission to check if a user has the required permission based on their role and the HTTP method.
    """

    def has_permission(self, request, view):
        """
        Checks if the user has permission for the requested HTTP method based on their role.
        """

        email = request.headers.get('X-User-Email')
        token = request.headers.get('X-Token')

        # Get the user's roles (assuming the roles are available in the user object)
        roles = self.user_adapter.get_role_by_user(email=email, token=token)

        # Check if the user's role is allowed to perform the requested HTTP method
        allowed_roles = RolePermissionMapping.get_allowed_roles_for_method(request.method)

        # If any of the user's roles are in the allowed roles for the requested method, grant permission
        for role in roles:
            if role in allowed_roles:
                return True

        return False

    def has_object_permission(self, request, view, obj):
        """
        Object-level permission check.
        Uses the same logic as `has_permission`.
        """
        return self.has_permission(request, view)
