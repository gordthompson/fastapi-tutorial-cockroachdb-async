from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Identity
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, Identity(start=1), primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)

    items = relationship(
        "Item", back_populates="owner", cascade="delete", passive_deletes=True
    )

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>"


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, Identity(start=1), primary_key=True, index=True)
    title = Column(String(255), index=True)
    description = Column(String(255), index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    owner = relationship("User", back_populates="items")

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return f"<Item(id={self.id}, title='{self.title}', owner_id={self.owner_id})>"
