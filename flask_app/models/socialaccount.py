import uuid

from sqlalchemy.dialects.postgresql import UUID

from db.postgres_db import PostgresBd, db


class SocialAccount(PostgresBd, db.Model):
    __tablename__ = "social_account"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    user = db.relationship("Users", backref=db.backref("social_accounts", lazy=True))
    social_name = db.Column(db.String(50), nullable=False)

    __table_args__ = (db.UniqueConstraint("user_id", "social_name", name="social_pk"),)

    def __repr__(self):
        return f"<SocialAccount {self.social_name}:{self.user_id}>"
