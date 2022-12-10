import uuid

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
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    is_superuser = db.Column(db.Boolean, default=False, nullable=False)
    device = db.relationship("Devices", secondary="history", lazy="dynamic")
    role = db.relationship("Roles", secondary="user_role", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.login}>"

    def hash_password(self):
        self.password = generate_password_hash(self.password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
