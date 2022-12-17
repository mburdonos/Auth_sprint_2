import uuid

from sqlalchemy.dialects.postgresql import UUID

from db.postgres_db import PostgresBd, db


class Roles(PostgresBd, db.Model):
    __tablename__ = "roles"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = db.Column(db.String(50), unique=True, nullable=False)
    user = db.relationship("Users", secondary="user_role", lazy="dynamic")
    permission = db.relationship(
        "Permissions", secondary="role_permission", lazy="dynamic"
    )

    def __repr__(self):
        return f"<Role {self.name}>"
