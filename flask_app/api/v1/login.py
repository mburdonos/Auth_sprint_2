from datetime import datetime, timedelta
from http import HTTPStatus
from json import dumps, loads

from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
)

from core.cache_conf import cache_client
from models.devices import Devices
from models.history import History
from models.users import Users
from utils.auth_utils import check_roles

login = Blueprint("login", __name__)


@login.route("/register", methods=["POST"])
def register():
    """Регистрация нового пользователя"""

    user = Users(**loads(request.data))
    if user.login and user.password:
        if user.get_first_raw({"login": user.login}):
            return jsonify({"msg": "login exist"}), HTTPStatus.UNAUTHORIZED
        else:
            user.hash_password()
            user.save_to_storage()

            response = jsonify({"msg": "create user successful"})
            return response, HTTPStatus.OK
    else:
        return jsonify({"msg": "login or password is empty"}), HTTPStatus.UNAUTHORIZED


@login.route("/login", methods=["POST"])
def log_in():
    login_user = Users(**loads(request.data))
    etalone_user = login_user.get_first_raw({"login": login_user.login})
    if etalone_user:
        if etalone_user.check_password(login_user.password):

            login_device = Devices(name=request.user_agent.string)
            if not login_device.get_first_raw({"name": login_device.name}):
                login_device.save_to_storage()
            else:
                login_device = login_device.get_first_raw({"name": login_device.name})

            History(
                user_id=etalone_user.id, device_id=login_device.id
            ).save_to_storage()

            additional_claims = {
                "user": login_user.login,
                "roles": [role.name for role in etalone_user.role.all()],
            }
            ret = {
                "access_token": create_access_token(
                    identity=login_user.login, additional_claims=additional_claims
                ),
                "refresh_token": create_refresh_token(
                    identity=login_user.login, additional_claims=additional_claims
                ),
            }

            response = jsonify(ret)
            access_token = ret["access_token"]

            current_date = datetime.now()
            ret["datetime_create_token"] = current_date.strftime("%Y-%m-%d %H:%M:%S")
            ret["datetime_end_token"] = (current_date + timedelta(hours=1)).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            ret["roles"] = [role.name for role in etalone_user.role.all()]
            ret["is_superuser"] = etalone_user.is_superuser
            cache_client.set(login_user.login, dumps(ret))

            set_access_cookies(response, access_token)

            return response, HTTPStatus.OK
        return jsonify({"msg": "not valid password"}), HTTPStatus.UNAUTHORIZED
    return jsonify({"msg": "not valid login"}), HTTPStatus.UNAUTHORIZED


@login.route("/logout", methods=["POST"])
@jwt_required()
def log_out():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response, HTTPStatus.OK


@login.route("/logout/all", methods=["POST"])
@jwt_required()
@check_roles(roles=["admin"])
def log_out_all():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response, HTTPStatus.OK


@login.route("/refresh", methods=["POST"])
@jwt_required()
@check_roles(roles=["admin", "staff"])
def refresh():
    identity = get_jwt_identity()
    user = Users().get_first_raw({"login": identity})
    get_cache_data = loads(cache_client.get(user.login))
    if get_cache_data["refresh_token"]:
        additional_claims = {
            "user": user.login,
            "roles": [role.name for role in user.role.all()],
        }
        ret = {
            "access_token": create_access_token(
                identity=user.login, additional_claims=additional_claims
            ),
            "refresh_token": create_refresh_token(
                identity=user.login, additional_claims=additional_claims
            ),
        }
        # get_cache_data["refresh_token"]
        response = jsonify(ret)

        current_date = datetime.now()
        ret["datetime_create_token"] = current_date.strftime("%Y-%m-%d %H:%M:%S")
        ret["datetime_end_token"] = (current_date + timedelta(hours=1)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        ret["roles"] = [role.name for role in user.role.all()]
        ret["is_superuser"] = user.is_superuser
        cache_client.set(user.login, dumps(ret))

        set_access_cookies(response, ret["access_token"])
        return response, HTTPStatus.OK


@login.route("/change_password", methods=["POST"])
@jwt_required()
def change_pass_word():
    identity = get_jwt_identity()
    user = Users().get_first_raw({"login": identity})
    data = loads(request.data)

    if (
        user.check_password(data["old_password"])
        and data["new_password"] == data["confirm_new_password"]
    ):
        user.password = data["new_password"]
        user.hash_password()
        user.save_to_storage()

        response = jsonify({"msg": "change password successful"})
        return response, HTTPStatus.OK
    return jsonify({"msg": "entered data is not correct"}), HTTPStatus.UNAUTHORIZED
