from sqlalchemy.orm import Session
from sqlalchemy import cast, Integer
import uuid
import datetime
from app.db.db_models import Post
from app.schemas import post as post_schema, user as user_schema


def create_post(db: Session, post: post_schema.PostCreate, post_additional_fields: dict, user: user_schema.UserOut):
    db_post = Post(
        uuid=uuid.uuid4(),
        userId=user.id,
        categoryId=post.categoryId,
        title=post.title,
        description=post.description,
        price=post.price,
        trade=post.trade,
        delivery=post.delivery,
        saveDeal=post.saveDeal,
        phoneHidden=post.phoneHidden,
        additionalFields=post_additional_fields,
        createdAt=datetime.datetime.utcnow()
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def create_dynamic_title(category):
    # qwe = db.query(Post).filter(cast(Post.additionalFields["mileage"], Integer) > 4).all()
    # print([qwer.id for qwer in qwe])
    # print("123")
    return "Dynamic Title"
