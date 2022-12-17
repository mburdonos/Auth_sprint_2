import uuid
from datetime import datetime

from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID

from db.postgres_db import PostgresBd, db


def create_partition(connection, **kw) -> None:
    """creating partition by user_sign_in"""
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "history_smart" PARTITION OF "history" FOR VALUES IN ('smart')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "history_mobile" PARTITION OF "history" FOR VALUES IN ('mobile')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "history_web" PARTITION OF "history" FOR VALUES IN ('web')"""
    )


class History(PostgresBd, db.Model):
    __tablename__ = "history"
    __table_args__ = (
        UniqueConstraint("id", "user_device_type"),
        {
            "postgresql_partition_by": "LIST (user_device_type)",
            "listeners": [("after_create", create_partition)],
        },
    )

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.id", ondelete="CASCADE")
    )
    device_id = db.Column(UUID(as_uuid=True), db.ForeignKey("devices.id"))
    datetime_login = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_device_type = db.Column(db.String(25), primary_key=True)
