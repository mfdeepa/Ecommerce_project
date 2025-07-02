class RolePermissionMapping:

    ROLE_PERMISSIONS = {
        'GET': ['Admin', 'Customer', 'Seller', 'Editor'],
        'POST': ['Admin', 'Seller'],
        'PUT': ['Admin', 'Seller', 'Editor'],
        'DELETE': ['Admin'],
    }

    @classmethod
    def get_allowed_roles_for_method(cls, method):

        return cls.ROLE_PERMISSIONS.get(method, [])

    @classmethod
    def add_permission_for_method(cls, method, roles):

        if method in cls.ROLE_PERMISSIONS:
            cls.ROLE_PERMISSIONS[method].extend(roles)
        else:
            cls.ROLE_PERMISSIONS[method] = roles

    @classmethod
    def remove_permission_for_method(cls, method, roles):

        if method in cls.ROLE_PERMISSIONS:
            cls.ROLE_PERMISSIONS[method] = [role for role in cls.ROLE_PERMISSIONS[method] if role not in roles]
