from models.permissions import Permissions
from models.role_permission import RolePermission
from models.roles import Roles


def create_base_permissions():
    """Создание базовых разрешений"""
    permissions = ["read", "write", "update", "delete"]
    for permission in permissions:
        current = Permissions(name=permission)
        if not current.get_first_raw({"name": current.name}):
            current.save_to_storage()


def create_base_roles():
    """Создание базовых ролей"""
    roles = {
        "admin": ["read", "write", "update", "delete"],
        "staff": ["read", "write", "update"],
        "user": ["read"],
    }
    # создать роли
    for role in roles:
        current = Roles(name=role)
        if not current.get_first_raw({"name": current.name}):
            current.save_to_storage()

            # создать права
            for permission in roles[role]:
                RolePermission(
                    role_id=current.get_first_raw({"name": current.name}).id,
                    permission_id=Permissions().get_first_raw({"name": permission}).id,
                ).save_to_storage()
