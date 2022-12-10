from functools import wraps
from json import loads
from typing import List

from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity

from core.cache_conf import cache_client
from models.roles import Roles
from models.user_role import UserRole
from models.users import Users


def create_admin_user():
    """Создание пользователя в правми admin"""
    user = Users(
        login="admin",
        password="admin",
        email="admin@gmail.com",
        first_name="Admin",
        last_name="Adminov",
    )
    if not user.get_first_raw({"login": user.login}):
        user.hash_password()
        user.save_to_storage()

        # добавить все роли для админа
        role = Roles().get_first_raw({"name": "admin"})
        UserRole(user_id=user.id, role_id=role.id).save_to_storage()


def check_roles(roles: List):
    """Декоратор проверка прав доступа"""

    def decorate(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # если был выполнен запрос, то выполняем проверку
            if request:
                user_name = get_jwt_identity()
                user_info = loads(cache_client.get(user_name))
                if user_info.get("is_superuser"):
                    return fn(*args, **kwargs)
                for role in user_info["roles"]:
                    if role in roles:
                        return fn(*args, **kwargs)
                return jsonify({"msg": "access is denied"})

        return wrapper

    return decorate
