from sqlalchemy import Column, Integer, String, TIMESTAMP, BOOLEAN, ForeignKey, BigInteger, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.session import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}
    id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    uuid = Column("uuid", UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    googleId = Column("google_id", String, unique=True)
    vkId = Column("vk_id", String, unique=True)
    appleId = Column("apple_id", String, unique=True)
    email = Column("email", String, unique=True)
    emailVerified = Column("email_verified", BOOLEAN, nullable=False)
    phone = Column("phone", String, unique=True)
    phoneVerified = Column("phone_verified", BOOLEAN, nullable=False)
    phoneHidden = Column("phone_hidden", BOOLEAN, nullable=False)
    password = Column("password", String)
    name = Column("name", String)
    surname = Column("surname", String)
    about = Column("about", String)
    username = Column("username", String, unique=True)
    rating = Column("rating", Integer)
    photoId = Column("photo_id", Integer, ForeignKey("public.users_photos.id"))
    roleId = Column("role_id", Integer, ForeignKey("public.roles.id"), nullable=False)
    createdAt = Column("created_at", TIMESTAMP, nullable=False)
    updatedAt = Column("updated_at", TIMESTAMP)
    lastLoginAt = Column("last_login_at", TIMESTAMP)
    deletedAt = Column("deleted_at", TIMESTAMP)
    emailVerifiedAt = Column("email_verified_at", TIMESTAMP)
    phoneVerifiedAt = Column("phone_verified_at", TIMESTAMP)

    photo = relationship("UserPhoto", back_populates="owner")
    role = relationship("Role", back_populates="owner")
    posts = relationship("Post", back_populates="user")


class UserPhoto(Base):
    __tablename__ = "users_photos"
    __table_args__ = {"schema": "public"}
    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    url = Column("url", String)

    owner = relationship("User", back_populates="photo")


class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": "public"}
    id = Column("id", Integer, primary_key=True, index=True, nullable=False)
    title = Column("title", String)

    owner = relationship("User", back_populates="role")


class Post(Base):
    __tablename__ = "posts"
    __table_args__ = {"schema": "public"}
    id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    uuid = Column("uuid", UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    userId = Column("user_id", Integer, ForeignKey("public.users.id"), nullable=False)
    title = Column("title", String, nullable=False)
    description = Column("description", String, nullable=False)
    price = Column("price", Float)
    trade = Column("trade", BOOLEAN, nullable=False)

    photos = relationship("PostPhoto", back_populates="owner")
    user = relationship("User", back_populates="posts")


class PostPhoto(Base):
    __tablename__ = "posts_photos"
    __table_args__ = {"schema": "public"}
    id = Column("id", Integer, primary_key=True, index=True, autoincrement=True, nullable=False)
    postId = Column("post_id", Integer, ForeignKey("public.posts.id"), nullable=False)
    url = Column("url", String)

    owner = relationship("Post", back_populates="photos")


class PhoneCalls(Base):
    __tablename__ = "phone_calls"
    __table_args__ = {"schema": "public"}
    id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    phone = Column("phone", String)
    validateCode = Column("validate_code", String)
    phoneValidate = Column("phone_validate", BOOLEAN, nullable=False)
    createdAt = Column("created_at", TIMESTAMP, nullable=False)


class PhoneVerifyUnsuccessfulTry(Base):
    __tablename__ = "phone_verify_unsuccessful_try"
    __table_args__ = {"schema": "public"}
    id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    phone = Column("phone", String)
    createdAt = Column("created_at", TIMESTAMP, nullable=False)
