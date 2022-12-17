import uuid

from sqlalchemy.dialects.postgresql import UUID

from db.postgres_db import PostgresBd, db


class UserRole(PostgresBd, db.Model):
    __tablename__ = "user_role"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.id", ondelete="CASCADE")
    )
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey("roles.id"))
