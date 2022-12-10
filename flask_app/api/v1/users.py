from http import HTTPStatus
from json import loads

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from models.devices import Devices
from models.history import History
from models.roles import Roles
from models.user_role import UserRole
from models.users import Users
from utils.auth_utils import check_roles
from utils.users_utils import valid_pagination

users = Blueprint("users", __name__)


@users.route("", methods=["GET"])
@jwt_required()
@check_roles(roles=["admin", "staff"])
def get_users():
    response = jsonify(
        {"all_users": [cur_user.login for cur_user in Users().get_all_raw()]}
    )
    return response, HTTPStatus.OK


@users.route("/history", methods=["GET"])
@jwt_required()
def get_history_user():
    pagination = valid_pagination(
        request.values.get("number"), request.values.get("size")
    )
    if pagination:
        current_user = Users().get_first_raw({"login": get_jwt_identity()})
        history = [
            {
                "user": Users().get_first_raw({"id": cur_history.user_id}).login,
                "device": Devices().get_first_raw({"id": cur_history.device_id}).name,
                "date_time": cur_history.datetime_login,
            }
            for cur_history in History().paginate_get_all_raw_with_filter(
                {"user_id": current_user.id}, pagination
            )
        ]
        return jsonify({"hystory": history}), HTTPStatus.OK
    return (
        jsonify(
            {
                "msg": "not valid pagination parameters, size: between 1 and 9999, number>=1 "
            }
        ),
        HTTPStatus.BAD_REQUEST,
    )


@users.route("/<user_name>/assign_role", methods=["POST"])
@jwt_required()
@check_roles(roles=["admin"])
def assign_role_for_users(user_name):
    data = loads(request.data)

    user = Users().get_first_raw({"login": user_name})
    user_roles = [role_cur.name for role_cur in user.role.all()]
    role = Roles().get_first_raw({"name": data["name"]})

    if role:
        if role.name not in user_roles:
            UserRole(user_id=user.id, role_id=role.id).save_to_storage()

            return jsonify({"msg": "role was added successfully"}), HTTPStatus.OK
        return jsonify({"msg": "current role exist for user"}), HTTPStatus.OK
    return jsonify({"msg": "current role not exist"}), HTTPStatus.UNAUTHORIZED


@users.route("/<user_name>/remove_role", methods=["POST"])
@jwt_required()
@check_roles(roles=["admin"])
def remove_role_for_users(user_name):
    data = loads(request.data)

    user = Users().get_first_raw({"login": user_name})
    user_roles = [role_cur.name for role_cur in user.role.all()]
    role = Roles().get_first_raw({"name": data["name"]})

    if role:
        if role.name in user_roles:
            user_role_cur = UserRole().get_first_raw(
                {"user_id": user.id, "role_id": role.id}
            )
            user_role_cur.delete_raw()

            return jsonify({"msg": "role was removed successfully"}), HTTPStatus.OK
        return jsonify({"msg": "current role not exist for user"}), HTTPStatus.OK
    return jsonify({"msg": "current role not exist"}), HTTPStatus.UNAUTHORIZED
