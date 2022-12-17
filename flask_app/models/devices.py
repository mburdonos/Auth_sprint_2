import uuid

from sqlalchemy.dialects.postgresql import UUID

from db.postgres_db import PostgresBd, db


class Devices(PostgresBd, db.Model):
    __tablename__ = "devices"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f"<Device {self.name}>"
