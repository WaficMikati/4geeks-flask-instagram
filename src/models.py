from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, Text, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional, Dict, Any

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean(), nullable=False, default=True)

    posts: Mapped[List["Post"]] = relationship(
        back_populates="author", cascade="all, delete-orphan")
    comments: Mapped[List["Comment"]] = relationship(
        back_populates="author", cascade="all, delete-orphan")
    likes: Mapped[List["Like"]] = relationship(
        back_populates="user", cascade="all, delete-orphan")

    def serialize(self) -> Dict[str, Any]:
        return {"id": self.id, "username": self.username, "email": self.email, "is_active": self.is_active}


class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    image_url: Mapped[str] = mapped_column(String(255), nullable=False)
    caption: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    author: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship(
        back_populates="post", cascade="all, delete-orphan")
    likes: Mapped[List["Like"]] = relationship(
        back_populates="post", cascade="all, delete-orphan")

    def serialize(self) -> Dict[str, Any]:
        return {"id": self.id, "author_id": self.author_id, "image_url": self.image_url, "caption": self.caption}


class Comment(db.Model):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey(
        "posts.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")

    def serialize(self) -> Dict[str, Any]:
        return {"id": self.id, "body": self.body, "author_id": self.author_id, "post_id": self.post_id}


class Like(db.Model):
    __tablename__ = "likes"
    __table_args__ = (UniqueConstraint(
        "user_id", "post_id", name="uq_user_post_like"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey(
        "posts.id", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship(back_populates="likes")
    post: Mapped["Post"] = relationship(back_populates="likes")

    def serialize(self) -> Dict[str, Any]:
        return {"id": self.id, "user_id": self.user_id, "post_id": self.post_id}
