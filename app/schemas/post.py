from pydantic import BaseModel
from uuid import UUID


class PostCreate(BaseModel):
    title: str
    description: str
    price: float
    trade: bool
    uuid: UUID
    class Config:
        orm_mode = True

class PostCreateRequest(BaseModel):
    title: str
    description: str
    price: float
    trade: bool

    class Config:
        orm_mode = True

class PostEdit(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    trade: bool | None = None
    uuid: UUID
    class Config:
        orm_mode = True

class PostEditRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    trade: bool | None = None
    class Config:
        orm_mode = True

class PostBlockMod(BaseModel):
    post_id: str
    user_id: str

class PostBlockPers(BaseModel):
    post_id: str
    user_id: str

class PostPhotos(BaseModel):
    id: int
    name: str | None = None
    url: str


# class Post(Base):
#     __tablename__ = "posts"
#     __table_args__ = {"schema": "public"}
#     id = Column("id", BigInteger, primary_key=True, index=True, autoincrement=True, unique=True, nullable=False)
#     uuid = Column("uuid", UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
#     userId = Column("user_id", BigInteger, ForeignKey("public.users.id"), nullable=False)
#     title = Column("title", String, nullable=False)
#     description = Column("description", String, nullable=False)
#     price = Column("price", Float)
#     trade = Column("trade", BOOLEAN, nullable=False)
#
#     photos = relationship("PostPhoto", back_populates="owner")
#     user = relationship("User", back_populates="posts")



