from sqlalchemy.orm import Session
import uuid
import datetime
from app.db.db_models import Post, PostsStatus, PostPhoto
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
        address=post.address,
        phoneHidden=post.phoneHidden,
        statusId=post.StatusId,
        additionalFields=post_additional_fields,
        createdAt=datetime.datetime.utcnow()
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def change_post_status(db: Session, post_id: int, status_id: int):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    db_status = db.query(PostsStatus).filter(PostsStatus.id == status_id).first()
    if not db_post:
        return False
    if not db_status:
        return False
    db_post.statusId = status_id
    db.commit()


def write_post_images_roads(db: Session, post_id: int, images_roads: list):
    images_roads_objects = [PostPhoto(road=x, postId=post_id, uuid=uuid.uuid4()) for x in images_roads]
    db.bulk_save_objects(images_roads_objects)
    db.commit()
    return True


def create_dynamic_title(category):
    return "Dynamic Title"


def get_post_by_id(db: Session, post_id: int):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post:
        return db_post
    else:
        return False


def get_post_out(db_post: Post):
    post_dict = db_post.__dict__
    post_out = post_schema.PostOut(**post_dict,
                                   status=db_post.status.__dict__,
                                   user=db_post.user.__dict__,
                                   photos=[x.__dict__ for x in db_post.photos])
    return post_out
