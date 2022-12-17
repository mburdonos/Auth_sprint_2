from http import HTTPStatus
from json import loads
from urllib.parse import urlencode

from flask import Blueprint, jsonify, redirect, request
from flask_jwt_extended import get_jwt_identity, jwt_required, unset_jwt_cookies
from requests import get, post

from core.cache_conf import cache_client
from core.config import configs
from models.socialaccount import SocialAccount
from models.users import Users
from utils.auth_utils import check_roles, login_process

login = Blueprint("login", __name__)


@login.route("/register", methods=["POST"])
def register():
    """Регистрация нового пользователя"""

    user = Users(**loads(request.data))
    if (user.login or user.email) and user.password:
        if user.get_user_by_universal_login(login=user.login, email=user.email):
            return jsonify({"msg": "login exist"}), HTTPStatus.UNAUTHORIZED
        else:
            user.hash_password()
            user.save_to_storage()

            response = jsonify({"msg": "create user successful"})
            return response, HTTPStatus.OK
    else:
        return jsonify({"msg": "login or password is empty"}), HTTPStatus.UNAUTHORIZED


@login.route("/register/<source>", methods=["POST"])
def register_source(source):
    """Регистрация нового пользователя через yandex"""

    user = Users(**loads(request.data))

    if user.get_user_by_universal_login(login=user.login, email=user.email):
        return jsonify({"msg": "this account exist"}), HTTPStatus.UNAUTHORIZED
    user.generate_random_password()
    user.save_to_storage()
    user_bd = user.get_first_raw({"login": user.login})
    if SocialAccount().get_first_raw({"user_id": str(user_bd.id)}):
        return (
            jsonify({"msg": "this account with source exist "}),
            HTTPStatus.UNAUTHORIZED,
        )
    SocialAccount(user_id=user_bd.id, social_name=source).save_to_storage()
    return jsonify({"msg": "create user successful"}), HTTPStatus.OK


@login.route("/login", methods=["POST"])
def log_in():
    login_user = Users(**loads(request.data))
    etalone_user = login_user.get_user_by_universal_login(
        login=login_user.login, email=login_user.email
    )
    if etalone_user:
        if etalone_user.check_password(login_user.password):
            return login_process(
                etalone_user=etalone_user, device_name=request.user_agent.string
            )

        return jsonify({"msg": "not valid password"}), HTTPStatus.UNAUTHORIZED
    return jsonify({"msg": "not valid login"}), HTTPStatus.UNAUTHORIZED


@login.route("/login/yandex", methods=["GET", "POST"])
def log_in_source():
    if request.args.get("code", False):
        data = {
            "grant_type": "authorization_code",
            "code": request.args.get("code"),
            "client_id": configs.yandex_client_id,
            "client_secret": configs.yandex_client_secret,
        }
        data = urlencode(data)
        return_data = post(configs.yandex_baseurl + "token", data).json()

        user_info_response = get(
            url=configs.yandex_info_url + "info",
            params={"jwt_secret": configs.yandex_client_secret},
            headers={"Authorization": f"OAuth {return_data.get('access_token')}"},
        )
        user_info = loads(user_info_response.text)
        device_name = user_info_response.request.headers.get("User-Agent")

        etalone_user = Users().get_user_by_universal_login(
            login=user_info.get("login"), email=user_info.get("default_email")
        )
        if etalone_user:
            return login_process(
                etalone_user=etalone_user,
                device_name=device_name,
                access_token=return_data.get("access_token"),
                refresh_token=return_data.get("refresh_token"),
            )
        return jsonify({"msg": "User not found"}), HTTPStatus.UNAUTHORIZED

    return redirect(
        configs.yandex_baseurl
        + "authorize?response_type=code&client_id={}".format(configs.yandex_client_id)
    )
    # return configs.yandex_baseurl + "authorize?response_type=code&client_id={}".format(configs.yandex_client_id)


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
        return login_process(etalone_user=user)


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


@login.route("/compare_permission", methods=["GET", "POST"])
@jwt_required()
def compare_permission():
    user_name = get_jwt_identity()
    user_info = loads(cache_client.get(user_name))
    return jsonify(user_info)
