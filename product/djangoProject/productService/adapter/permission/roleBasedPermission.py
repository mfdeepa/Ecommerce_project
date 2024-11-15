from rest_framework.permissions import BasePermission

from productService.adapter.permission.rolePermissionMapping import RolePermissionMapping
from productService.adapter.useradapter import UserAdapter


# class RoleBasedPermission(BasePermission):
#     """
#     Custom permission to check if a user has the required permission based on their role and the HTTP method.
#     """
#
    # def has_permission(self, request, view):
    #     """
    #     Checks if the user has permission for the requested HTTP method based on their role.
    #     """
    #     user = request.user
    #     email = request.user.email
    #     token = request.user.token
    #
    #     # Ensure the user is authenticated
    #     if not user.is_authenticated:
    #         return False
    #
    #     # Get the user's roles (assuming the roles are available in the user object)
    #     roles = UserAdapter.get_role_by_user(email=email, token=token)
    #
    #     # Check if the user's role is allowed to perform the requested HTTP method
    #     allowed_roles = RolePermissionMapping.get_allowed_roles_for_method(request.method)
    #
    #     # If any of the user's roles are in the allowed roles for the requested method, grant permission
    #     for role in roles:
    #         if role in allowed_roles:
    #             return True
    #
    #     # If no matching role is found, deny permission
    #     return False
    #
    # def has_object_permission(self, request, view, obj):
    #     """
    #     Object-level permission check.
    #     Uses the same logic as `has_permission`.
    #     """
    #     return self.has_permission(request, view)


class RoleBasedPermission(BasePermission):
    def has_permission(self, request, view):
        # Get token from request header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return False

        token = auth_header.split(' ')[1]
        email = request.headers.get('X-User-Email')

        if not email or not token:
            return False

        # Get the user's roles
        roles = UserAdapter.get_role_by_user(email=email, token=token)

        if not roles or isinstance(roles, dict) and 'error' in roles:
            return False

        # Check if the user's role is allowed
        allowed_roles = RolePermissionMapping.get_allowed_roles_for_method(request.method)
        return any(role in allowed_roles for role in roles)
