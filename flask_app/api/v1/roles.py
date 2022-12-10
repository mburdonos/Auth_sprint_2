from http import HTTPStatus
from json import loads

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from models.role_permission import RolePermission
from models.roles import Roles
from utils.auth_utils import check_roles

roles = Blueprint("roles", __name__, template_folder="templates")


@roles.route("", methods=["GET"])
@jwt_required()
@check_roles(roles=["admin", "staff"])
def get_all_role():
    return {"roles": [role.name for role in Roles().get_all_raw()]}, HTTPStatus.OK


@roles.route("/create", methods=["POST"])
@jwt_required()
@check_roles(roles=["admin"])
def create_role():
    role = Roles(**loads(request.data))
    role.save_to_storage()
    return jsonify({"msg": "role was added successfully"}), HTTPStatus.OK


@roles.route("/delete", methods=["DELETE"])
@jwt_required()
@check_roles(roles=["admin"])
def delete_role():
    role = Roles(**loads(request.data))
    role = role.get_first_raw({"name": role.name})

    if role:
        relation_role = RolePermission().get_all_raw_with_filter({"role_id": role.id})
        for relation in relation_role:
            relation.delete_raw()

        role.delete_raw()
    return jsonify({"msg": "role was successfully removed"}), HTTPStatus.OK


@roles.route("/update", methods=["PUT"])
@jwt_required()
@check_roles(roles=["admin"])
def update_role():
    data = loads(request.data)
    role = Roles().get_first_raw({"name": data["old_role"]})

    if role:
        role.name = data["new_role"]
        role.save_to_storage()
    return jsonify({"msg": "role was successfully updated"}), HTTPStatus.OK
