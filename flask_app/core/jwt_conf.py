from datetime import timedelta

from flask import Flask
from flask_jwt_extended import JWTManager

from core.config import configs

jwt = JWTManager()


def jwt_init(app: Flask):
    """Инициализация jwt"""
    app.config["JWT_SECRET_KEY"] = configs.secret_key
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
    app.config["JWT_COOKIE_CSRF_PROTECT"] = False
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
    jwt.init_app(app)
