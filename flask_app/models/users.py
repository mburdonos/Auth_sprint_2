import string
import uuid
from secrets import choice as secrets_choice
from typing import Optional

from sqlalchemy import or_
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import check_password_hash, generate_password_hash

from db.postgres_db import PostgresBd, db


class Users(PostgresBd, db.Model):
    __tablename__ = "users"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    login = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    is_superuser = db.Column(db.Boolean, default=False, nullable=False)
    device = db.relationship("Devices", secondary="history", lazy="dynamic")
    role = db.relationship("Roles", secondary="user_role", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.login}>"

    def get_user_by_universal_login(
        self, login: Optional[str] = None, email: Optional[str] = None
    ):
        return self.query.filter(
            or_(Users.login == login, Users.email == email)
        ).first()

    def generate_random_password(self):
        alphabet = string.ascii_letters + string.digits
        self.password = "".join(secrets_choice(alphabet) for _ in range(16))

    def hash_password(self):
        self.password = generate_password_hash(self.password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
