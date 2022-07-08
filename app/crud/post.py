from sqlalchemy.orm import Session
from fastapi import Depends
import uuid
import datetime
from app.api.dependencies import get_db
from app.db.db_models import Post, PostPhoto, Block_mod, Block_pers
from app.schemas import post as post_schema
from app.utils import security
from app.api import dependencies
from sqlalchemy import select


def create_post(db: Session, post: post_schema.PostCreate, user_id_out:int):
    db_post = Post(
        title=post.title,
        description=post.description,
        price=post.price,
        trade=post.trade,
        uuid=uuid.uuid4(),
        userId=user_id_out
    )
    db.add(db_post)
    db.commit()
    return True

def get_post_out(db: Session, post_id:int):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post:
        return db_post
    else: return False

def get_post_view(db: Session, post_id:int):
    db_post = db.query(Post.id, Post.title, Post.price, Post.description, Post.trade).filter(Post.id == post_id).first()
    if db_post:
        return db_post
    else: return False

def get_post_view_all(db: Session, user_id:int):
    blocked_posts = db.query(Block_pers.post_id).where(Block_pers.user_id == user_id).all()
    blocked_posts = [r[0] for r in blocked_posts]
    blocked_posts_mod = db.query(Block_mod.post_id).all()
    if (isinstance(blocked_posts_mod, int)) == True:
        all_blocked_posts = blocked_posts_mod.append(blocked_posts)
    else:
        blocked_posts_mod = [r[0] for r in blocked_posts_mod]
        all_blocked_posts = blocked_posts_mod + blocked_posts
    all_blocked_posts = blocked_posts_mod + blocked_posts
    db_post = db.query(Post.id, Post.title, Post.price, Post.description, Post.trade).filter(Post.id.not_in(all_blocked_posts)).all()
    if db_post:
        return db_post
    else: return False




def create_block_pers(db: Session, user_id:int, post_id: int):
    db_block = Block_pers(
        user_id=user_id,
        post_id=post_id,
        time_op=datetime.datetime.utcnow()
    )
    db.add(db_block)
    db.commit()
    return True

def create_block_mod(db: Session, user_id:int, post_id: int):
    db_block = Block_mod(
        user_id=user_id,
        post_id=post_id,
        time_op=datetime.datetime.utcnow()
    )
    db.add(db_block)
    db.commit()
    return True