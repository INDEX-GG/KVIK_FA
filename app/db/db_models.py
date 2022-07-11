from sqlalchemy import Column, Integer, String, TIMESTAMP, BOOLEAN, ForeignKey, BigInteger, JSON, FLOAT
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
    photoId = Column("photo_id", BigInteger, ForeignKey("public.users_photos.id"))
    roleId = Column("role_id", BigInteger, ForeignKey("public.roles.id"))
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
    id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=True, nullable=False)
    url = Column("url", String)

    owner = relationship("User", back_populates="photo")


class Role(Base):
    __tablename__ = "roles"
    __table_args__ = {"schema": "public"}
    id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=False, nullable=False)
    title = Column("title", String)

    owner = relationship("User", back_populates="role")


class Post(Base):
    __tablename__ = "posts"
    __table_args__ = {"schema": "public"}
    id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    uuid = Column("uuid", UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    userId = Column("user_id", BigInteger, ForeignKey("public.users.id"), nullable=False)
    categoryId = Column("category_id", BigInteger, ForeignKey("categories.posting_categories.id"))
    title = Column("title", String, nullable=False)
    description = Column("description", String, nullable=False)
    price = Column("price", Integer)
    trade = Column("trade", BOOLEAN, nullable=False)
    delivery = Column("delivery", BOOLEAN, nullable=False)
    saveDeal = Column("save_deal", BOOLEAN, nullable=False)
    phoneHidden = Column("phone_hidden", BOOLEAN, nullable=False)
    # status = Column("status")
    # address = Column("address")
    createdAt = Column("created_at", TIMESTAMP, nullable=False)
    updatedAt = Column("updated_at", TIMESTAMP)

    photos = relationship("PostPhoto", back_populates="owner")
    user = relationship("User", back_populates="posts")


class PostPhoto(Base):
    __tablename__ = "posts_photos"
    __table_args__ = {"schema": "public"}
    id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=True, nullable=False)
    postId = Column("post_id", BigInteger, ForeignKey("public.posts.id"), nullable=False)
    url = Column("url", String)

    owner = relationship("Post", back_populates="photos")


class PhoneCall(Base):
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


class Catalog(Base):
    __tablename__ = "catalog"
    __table_args__ = {"schema": "categories"}
    id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    parentId = Column("parent_id", BigInteger, ForeignKey("categories.catalog.id"))
    patch = Column("patch", String, nullable=False)
    title = Column("title", String, nullable=False)
    transTitle = Column("trans_title", String, nullable=False)
    postingPatch = Column("posting_patch", String, nullable=False)
    postingTitle = Column("posting_title", String, nullable=False)
    transPostingTitle = Column("trans_posting_title", String, nullable=False)


class PostingCategories(Base):
    __tablename__ = "posting_categories"
    __table_args__ = {"schema": "categories"}
    id = Column("id", BigInteger, ForeignKey("categories.catalog.id"), primary_key=True, index=True,
                autoincrement=False, unique=True, nullable=False)
    patch = Column("patch", String, nullable=False)
    title = Column("title", String, nullable=False)
    transTitle = Column("trans_title", String, nullable=False)
    postingPatch = Column("posting_patch", String, nullable=False)
    postingTitle = Column("posting_title", String, nullable=False)
    transPostingTitle = Column("trans_posting_title", String, nullable=False)
    dynamicTitle = Column("dynamic_title", String, nullable=False)
    additionalFields = Column("additional_fields", JSON, nullable=False)


class Car(Base):
    __tablename__ = "cars"
    __table_args__ = {"schema": "vehicles"}
    id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    markId = Column("mark_id", BigInteger, ForeignKey("vehicles.cars_marks.id"), nullable=False)
    mark = Column("mark", String, nullable=False)
    model = Column("model", String, nullable=False)
    generation = Column("generation", String, nullable=False)
    modification = Column("modification", String, nullable=False)
    yearFrom = Column("year_from", Integer, nullable=False)
    yearTo = Column("year_to", Integer, nullable=False)
    fuelType = Column("fuel_type", String, nullable=False)
    driveType = Column("drive_type", String, nullable=False)
    transmission = Column("transmission", String, nullable=False)
    power = Column("power", Integer, nullable=False)
    engineSize = Column("engine_size", FLOAT, nullable=False)
    bodyType = Column("body_type", String, nullable=False)
    doors = Column("doors", Integer, nullable=False)
    complectation = Column("complectation", String, nullable=False)


class CarMark(Base):
    __tablename__ = "cars_marks"
    __table_args__ = {"schema": "vehicles"}
    id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
    title = Column("title", String, unique=True, nullable=False)
