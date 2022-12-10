import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID

from db.postgres_db import PostgresBd, db


class History(PostgresBd, db.Model):
    __tablename__ = "history"

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
    device_id = db.Column(UUID(as_uuid=True), db.ForeignKey("devices.id"))
    datetime_login = db.Column(db.DateTime, nullable=False, default=datetime.now())
