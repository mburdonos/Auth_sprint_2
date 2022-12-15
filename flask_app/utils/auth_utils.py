import random
from datetime import datetime, timedelta
from functools import wraps
from http import HTTPStatus
from json import dumps, loads
from typing import List, Optional

from flask import jsonify, request
from flask_jwt_extended import (create_access_token, create_refresh_token,
                                get_jwt, get_jwt_identity, jwt_required,
                                set_access_cookies, unset_jwt_cookies)

from core.cache_conf import cache_client
from models.devices import Devices
from models.history import History
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


def login_process(
    etalone_user: Users,
    device_name: Optional[str] = None,
    access_token: Optional[str] = None,
    refresh_token: Optional[str] = None,
):
    if device_name:
        login_device = Devices(name=device_name)
        if not login_device.get_first_raw({"name": login_device.name}):
            login_device.save_to_storage()
        else:
            login_device = login_device.get_first_raw({"name": login_device.name})

        # выбор случайного устройства из списка (сделано для тестирования, чтобы заносить разные записи)
        device_type = random.choice(["web", "mobile", "smart"])

        History(
            user_id=etalone_user.id,
            device_id=login_device.id,
            user_device_type=device_type,
        ).save_to_storage()

    additional_claims = {
        "user": etalone_user.login,
        "roles": [role.name for role in etalone_user.role.all()],
    }
    if not access_token:
        access_token = create_access_token(
            identity=etalone_user.login, additional_claims=additional_claims
        )
    if not refresh_token:
        refresh_token = create_refresh_token(
            identity=etalone_user.login, additional_claims=additional_claims
        )
    ret = {"access_token": access_token, "refresh_token": refresh_token}

    response = jsonify(ret)
    access_token = ret["access_token"]

    current_date = datetime.now()
    ret["datetime_create_token"] = current_date.strftime("%Y-%m-%d %H:%M:%S")
    ret["datetime_end_token"] = (current_date + timedelta(hours=1)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )
    ret["roles"] = [role.name for role in etalone_user.role.all()]
    ret["is_superuser"] = etalone_user.is_superuser
    cache_client.set(etalone_user.login, dumps(ret))

    set_access_cookies(response, access_token)

    return response, HTTPStatus.OK


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
