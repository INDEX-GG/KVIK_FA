from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.crud import post as post_crud
from app.crud import user as users_crud
from app.schemas import post as post_schema
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

@router.post("/mod", summary="Blocking a post by moderator",
            description="")
async def block_post_mod(post_id:int,
                    db: Session = Depends(get_db), user=Depends(users_crud.get_current_user)):
    user_id = int(user.id)
    new_block = post_crud.create_block_mod(db = db, user_id=user_id, post_id=post_id)
    if new_block:
        return {"message": "success"}
    else:
        return {"message" : "failure"}


@router.put("/{post_id}", summary="Editing a post",
            description="")
async def edit_post(post_id:int, post_data: post_schema.PostEditRequest,
                    db: Session = Depends(get_db), user=Depends(users_crud.get_current_user)):
    post_edited = post_crud.get_post_out(db=db, post_id = post_id)
    if post_edited.userId == user.id:
        edit = post_crud.update_post(db=db, post_data=post_data, post_id=post_id)
        if edit:
            return {"message": "success"}
        else:
            return {"message": "failure"}

@router.get("/{post_id}", summary="Viewing a particular post",
            description="")
async def view_post(post_id:int,
                    db: Session = Depends(get_db)):
    post_edited :dict = post_crud.get_post_view(db=db, post_id = post_id)
    post_edited = jsonable_encoder(post_edited)
    return JSONResponse(content=[post_edited])

@router.get("", summary="Viewing all posts",
            description="")
async def view_posts(db: Session = Depends(get_db), user=Depends(users_crud.get_current_user)):
    user_id = int(user.id)
    post_edited :dict = post_crud.get_post_view_all(db=db, user_id = user_id)
    post_edited = jsonable_encoder(post_edited)
    return JSONResponse(content=[post_edited])

@router.post("", summary="Blocking a particular post for yourself",
            description="")
async def block_post_pers(post_id:int,
                    db: Session = Depends(get_db), user=Depends(users_crud.get_current_user)):
    user_id = int(user.id)
    post_block = post_crud.get_post_out(db=db, post_id=post_id)
    if post_block.userId == user.id:
        new_block = post_crud.create_block_pers(db = db, user_id=user_id, post_id=post_id)
        if new_block:
            return {"message": "success"}
        else:
            return {"message" : "failure"}
