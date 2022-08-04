from sqlalchemy.orm import Session, joinedload
import uuid
import datetime
from typing import List
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
        statusId=post.statusId,
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


def delete_post_images_roads(db: Session, post_id: int):
    db.query(PostPhoto).where(PostPhoto.postId == post_id).delete()
    db.commit()
    return True


def create_dynamic_title(category):
    return "Dynamic Title"


def get_post_by_id(db: Session, post_id: int):
    db_post = db.query(Post).options(joinedload("photos")).options(joinedload("user")).options(joinedload("status"))\
        .filter(Post.id == post_id).first()
    if db_post:
        return db_post
    else:
        return False


def get_user_post_by_id(db: Session, post_id: int, user_id: int):
    db_post = db.query(Post).options(joinedload("photos")).options(joinedload("user")).options(joinedload("status"))\
        .filter(Post.id == post_id, Post.userId == user_id).first()
    if db_post:
        return db_post
    else:
        return False


def get_post_out(db_post: Post):
    post_dict = db_post.__dict__
    post_dict["status"] = db_post.status.__dict__
    post_dict["user"] = db_post.user.__dict__
    post_dict["photos"] = [x.__dict__ for x in db_post.photos]
    post_out = post_schema.PostOut(**post_dict)
    return post_out


def get_post_in_detail_out(db_post: Post, category):
    post_dict = db_post.__dict__
    new_post_additional_fields = {}
    for field in category.additionalFields:
        if field["alias"] in db_post.additionalFields:
            new_post_additional_fields[field["alias"]] = {
                "title": field["title"],
                "value": db_post.additionalFields[field["alias"]]
            }
    post_dict["additionalFields"] = new_post_additional_fields
    post_dict["status"] = db_post.status.__dict__
    post_dict["user"] = db_post.user.__dict__
    post_dict["photos"] = [x.__dict__ for x in db_post.photos]
    post_dict["category"] = category.__dict__
    post_out = post_schema.PostInDetailOut(**post_dict)
    return post_out


def get_posts_out(db_posts: List[Post]):
    posts_out = []
    for db_post in db_posts:
        posts_out.append(get_post_out(db_post))
    return posts_out


def get_posts(db: Session):
    db_posts = db.query(Post)\
        .options(joinedload("photos"))\
        .options(joinedload("user"))\
        .options(joinedload("status"))\
        .order_by(Post.id.desc()).limit(30).all()
    return db_posts


def edit_post(db: Session, db_post: Post, edited_additional_fields: dict, post_data: post_schema.PostEdit):

    db_post.additionalFields = edited_additional_fields
    db_post.statusId = post_data.statusId
    db_post.updatedAt = datetime.datetime.utcnow()

    if post_data.title is not None:
        db_post.title = post_data.title
    if post_data.description is not None:
        db_post.description = post_data.description
    if post_data.price is not None:
        db_post.price = post_data.price
    if post_data.trade is not None:
        db_post.trade = post_data.trade
    if post_data.phoneHidden is not None:
        db_post.phoneHidden = post_data.phoneHidden
    if post_data.delivery is not None:
        db_post.delivery = post_data.delivery
    if post_data.saveDeal is not None:
        db_post.saveDeal = post_data.saveDeal
    if post_data.address is not None:
        db_post.address = post_data.address

    db.commit()

    return True


def get_edited_additional_fields(post, edited_fields):
    post_fields = post.additionalFields.copy()
    for field in post_fields:
        if field in edited_fields:
            post_fields[field] = edited_fields[field]
    return post_fields
