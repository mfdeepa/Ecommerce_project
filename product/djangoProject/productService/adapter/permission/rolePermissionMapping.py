# role_permission_mapping.py

class RolePermissionMapping:
    """
    Class to manage roles and their associated HTTP permissions, with separate mappings for each HTTP method.
    """

    ROLE_PERMISSIONS = {
        'GET': ['Admin', 'Customer', 'Seller', 'Editor'],  # All roles can read (GET)
        'POST': ['Admin', 'Seller'],  # Only admin and seller can create (POST)
        'PUT': ['Admin', 'Seller', 'Editor'],  # Admin, seller, and editor can update (PUT)
        'DELETE': ['Admin'],  # Only admin can delete (DELETE)
    }

    @classmethod
    def get_allowed_roles_for_method(cls, method):
        """
        Returns the allowed roles for a given HTTP method (GET, POST, PUT, DELETE).
        """
        return cls.ROLE_PERMISSIONS.get(method, [])

    @classmethod
    def add_permission_for_method(cls, method, roles):
        """
        Adds roles to the list of roles allowed to perform a specific HTTP method.
        """
        if method in cls.ROLE_PERMISSIONS:
            cls.ROLE_PERMISSIONS[method].extend(roles)
        else:
            cls.ROLE_PERMISSIONS[method] = roles

    @classmethod
    def remove_permission_for_method(cls, method, roles):
        """
        Removes roles from the list of roles allowed to perform a specific HTTP method.
        """
        if method in cls.ROLE_PERMISSIONS:
            cls.ROLE_PERMISSIONS[method] = [role for role in cls.ROLE_PERMISSIONS[method] if role not in roles]
