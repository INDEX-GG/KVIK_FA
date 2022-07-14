import datetime
import os
import uuid

from PIL import Image
from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.db.db_models import Post, PostPhoto, Block_mod, Block_pers, User
from app.schemas import post as post_schema


def create_post(db: Session, post: post_schema.PostCreate, user_id_out: int):
    db_post = Post(
        title=post.title,
        description=post.description,
        price=post.price,
        trade=post.trade,
        uuid=uuid.uuid4(),
        userId=user_id_out,
    )
    db.add(db_post)
    db.commit()
    return True


def update_post(db: Session, post_data: post_schema.PostEditRequest, post_id: int):
    edited_post = db.query(Post).filter(Post.id == post_id).first()
    if post_data.title is not None:
        edited_post.title = post_data.title
    if post_data.description is not None:
        edited_post.description = post_data.description
    if post_data.price is not None:
        edited_post.price = post_data.price
    if post_data.trade is not None:
        edited_post.trade = post_data.trade
        db.commit()
        return True
    else:
        return False


def get_post_out(db: Session, post_id: int):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post:
        return db_post
    else:
        return False


def get_post_view(db: Session, post_id: int):
    db_post = db.query(Post.id, Post.title, Post.price, Post.description, Post.trade, User.username).join(User).\
        filter((User.id == Post.userId)).filter(Post.id == post_id).first()
    if db_post:
        return db_post
    else:
        return False


def get_post_view_all(db: Session, user_id: int):
    all_blocked_posts = get_block_post(db=db, user_id=user_id)
    db_post = db.query(Post.id, Post.title, Post.price, Post.description, Post.trade, User.username). \
        join(User).filter((User.id == Post.userId)).filter(
        Post.id.not_in(all_blocked_posts)).all()
    if db_post:
        return db_post
    else:
        return False


def get_block_post(db: Session, user_id: int):
    blocked_posts = db.query(Block_pers.post_id).where(Block_pers.user_id == user_id).all()
    blocked_posts = [r[0] for r in blocked_posts]
    blocked_posts_mod = db.query(Block_mod.post_id).all()
    if isinstance(blocked_posts_mod, int):
        all_blocked_posts = blocked_posts_mod.append(blocked_posts)
    else:
        blocked_posts_mod = [r[0] for r in blocked_posts_mod]
        all_blocked_posts = blocked_posts_mod + blocked_posts
    return all_blocked_posts


def create_block_pers(db: Session, user_id: int, post_id: int):
    db_block = Block_pers(
        user_id=user_id,
        post_id=post_id,
        time_op=datetime.datetime.utcnow()
    )
    db.add(db_block)
    db.commit()
    return True


def create_block_mod(db: Session, user_id: int, post_id: int):
    db_block = Block_mod(
        user_id=user_id,
        post_id=post_id,
        time_op=datetime.datetime.utcnow()
    )
    db.add(db_block)
    db.commit()
    return True


def create_file_record(db: Session, post_id: int, url: str):
    db_file_rec = PostPhoto(
        postId=post_id,
        url=url,
    )
    db.add(db_file_rec)
    db.commit()
    return True


def get_file_out(db: Session, post_id: int, photo_id: str):
    db_file: str = db.query(PostPhoto.url).filter(PostPhoto.postId == post_id). \
        filter(PostPhoto.id == photo_id).first()
    return db_file


def save_photo(file:UploadFile, im:Image):
    file_uuid = str(uuid.uuid4())
    ext = file.filename[file.filename.rfind("."):]
    filename = file_uuid + ext
    print(filename)
    im.save(filename)
    return filename


def get_file_path(file_name: str):
    path: str = repr(file_name)
    path = path.replace("'", '')
    path = path.replace('(', '')
    path = path.replace(')', '')
    path = path.replace(",", '')
    path = path.replace('"', '')
    path_rel = os.getcwd()
    os.path.join(path_rel, '')
    path_rel = os.path.join(path_rel, path)
    return path_rel
