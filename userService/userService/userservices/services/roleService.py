
from userservices.models import Role


class RolesService:

    def create_role(self, name: str):
        role = Role.objects.filter(name=name).first()
        if role is not None:
            raise Exception("Role already exists")

        role = Role(name=name)
        role.save()
        return role
