from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.crud import post as post_crud
from app.crud import user as users_crud
# from app.schemas import post as post_schema, response as response_schema
from app.schemas import post as post_schema
from app.db.db_models import User, UserPhoto, Post
from app.schemas import user as user_schema
from app.utils import security
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("", summary="Uploading a post",
             description="")
async def create_post(post_data: post_schema.PostCreateRequest,
                      user=Depends(users_crud.get_current_user),
                      db: Session = Depends(get_db)):
    user_id = int(user.id)
    new_post = post_crud.create_post(post=post_data, db=db, user_id_out=user_id)
    return {"message": "success"}


@router.put("/{post_id}", summary="Editing a post",
            description="")
async def edit_post(post_data: post_schema.PostEditRequest,post_id:int,
                    db: Session = Depends(get_db), user=Depends(users_crud.get_current_user)):
    post_edited = post_crud.get_post_out(db=db, post_id = post_id)
    if post_edited.userId == user.id:
        x = db.query(Post).filter(Post.id == post_id).first()
        if post_data.title is not None:
            x.title: str = post_data.title
        if post_data.description is not None:
            x.description: str = post_data.description
        if post_data.price is not None:
            x.price: float = post_data.price
        if post_data.trade is not None:
            x.trade: bool = post_data.trade
        db.commit()
        return {"message": "success"}
    else:
        return {"message": "failure"}

@router.get("/{post_id}", summary="Viewing a particular post",
            description="")
async def view_post(post_id:int,
                    db: Session = Depends(get_db), user=Depends(users_crud.get_current_user)):
    post_edited :dict = post_crud.get_post_view(db=db, post_id = post_id)
    post_edited = jsonable_encoder(post_edited)
    return JSONResponse(content=[post_edited])

@router.get("", summary="Viewing all posts",
            description="")
async def view_posts(db: Session = Depends(get_db), user=Depends(users_crud.get_current_user)):
    post_edited :dict = post_crud.get_post_view_all(db=db)
    post_edited = jsonable_encoder(post_edited)
    return JSONResponse(content=[post_edited])

