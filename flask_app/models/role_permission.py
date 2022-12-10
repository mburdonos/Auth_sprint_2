import uuid

from sqlalchemy.dialects.postgresql import UUID

from db.postgres_db import PostgresBd, db


class RolePermission(PostgresBd, db.Model):
    __tablename__ = "role_permission"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey("roles.id"))
    permission_id = db.Column(UUID(as_uuid=True), db.ForeignKey("permissions.id"))
