import uuid

from sqlalchemy.dialects.postgresql import UUID

from db.postgres_db import PostgresBd, db


class Permissions(PostgresBd, db.Model):
    __tablename__ = "permissions"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"<Permission {self.name}>"
