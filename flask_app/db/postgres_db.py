from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from core.config import configs
from db.storage import Storage

db = SQLAlchemy()


def init_storage(app: Flask):
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = f"{configs.storage_driver}://{configs.pg_user}:{configs.pg_password}@{configs.pg_host}/{configs.pg_database}"
    db.init_app(app)


class PostgresBd(Storage):
    def save_to_storage(self):
        db.session.add(self)
        db.session.commit()

    def get_all_raw_with_filter(self, filters: dict):
        return self.query.filter_by(**filters).all()

    def get_all_raw(self):
        return self.query.all()

    def get_first_raw(self, filters: dict):
        return self.query.filter_by(**filters).first()

    def delete_raw(self):
        db.session.delete(self)
        db.session.commit()

    def paginate_get_all_raw_with_filter(self, filters: dict, pagination: dict):
        return self.query.filter_by(**filters).paginate(
            page=pagination["number"], per_page=pagination["size"]
        )
