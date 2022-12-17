from gevent import monkey

monkey.patch_all()

import click
from flask import Flask, request
from gevent.pywsgi import WSGIServer
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from sqlalchemy import create_engine

from api.v1.login import login
from api.v1.roles import roles
from api.v1.users import users
from core.cache_conf import cache_init
from core.config import configs
from core.jwt_conf import jwt_init
from db.postgres_db import init_storage
from models.history import create_partition
from models.users import Users
from utils.jaeger import configure_tracer
from utils.roles_utils import create_base_permissions, create_base_roles

app = Flask(__name__)
app.app_context().push()

if configs.enable_tracer:
    configure_tracer()
    FlaskInstrumentor().instrument_app(app)

    @app.before_request
    def before_request():
        request_id = request.headers.get("X-Request-Id")
        if not request_id:
            raise RuntimeError("request id is required")


init_storage(app)
cache_init(app)
jwt_init(app)
create_partition(connection=create_engine(app.config["SQLALCHEMY_DATABASE_URI"]))


@app.cli.command("create-superuser")
@click.argument("login")
@click.argument("password")
@click.argument("email")
@click.argument("first_name")
@click.argument("last_name")
def create_super_user(login, password, email, first_name, last_name):
    if not Users().get_first_raw({"login": login}):
        user = Users(
            login=login,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_superuser=True,
        )
        user.hash_password()
        user.save_to_storage()


def main():
    app.register_blueprint(login, url_prefix="/api/v1/auth")
    app.register_blueprint(users, url_prefix="/api/v1/auth/users")
    app.register_blueprint(roles, url_prefix="/api/v1/auth/roles")

    create_base_permissions()
    create_base_roles()

    app.run(debug=configs.debug, host="0.0.0.0")
    http_server = WSGIServer(("", 5000), app)
    http_server.serve_forever()


if __name__ == "__main__":
    main()
