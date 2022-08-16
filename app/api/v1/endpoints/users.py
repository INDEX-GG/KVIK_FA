from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.db.db_models import User
from app.crud import user as users_crud, post as post_crud
from app.schemas import user as user_schema, response as response_schema, post as post_schema
from app.schemas.response import custom_errors
from app.utils import security


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", summary="Registration user",
             response_model=response_schema.ResponseSuccess, status_code=201,
             responses={409: custom_errors("Conflict", [{"msg": "User with this phone already exist"}])
                        })
async def registration(user_data: user_schema.UserCreateResponse,
                       user_phone: str = Depends(security.decode_phone_token),
                       db: Session = Depends(get_db)):
    user = user_schema.UserCreate(**user_data.__dict__, phone=user_phone)
    new_user = users_crud.create_user(user=user, db=db)
    if not new_user:
        raise HTTPException(status_code=409, detail={"msg": "User with this phone already exist"})
    return {"msg": "success"}


@router.get("/{user_id}", summary="Get User By Id",
            response_model=user_schema.UserOut
            )
async def get_user_by_id(user_id: int,  db: Session = Depends(get_db)):
    db_user: User = users_crud.get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(404)
    user_out = users_crud.get_user_out(db_user=db_user)
    return user_out


@router.get("/{user_id}/posts", summary="Get User Posts",
            response_model=user_schema.UserPostsOut
            )
async def get_user_by_id(user_id: int, params: post_schema.PostsPagination = Depends(), db: Session = Depends(get_db)):
    db_user: User = users_crud.get_user_by_id(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(404)
    user_out = users_crud.get_user_out(db_user=db_user)
    db_posts = post_crud.get_user_posts(db=db, page=params.page, user_id=user_id)
    posts_out = post_crud.get_posts_out(db_posts)
    user_with_posts = user_schema.UserPostsOut(user=user_out, posts=posts_out)
    return user_with_posts


@router.get("/me", summary="Get Current User",
            response_model=user_schema.UserOut)
async def read_users_me(current_user: dict = Depends(users_crud.get_current_user)):
    return current_user


# @router.put("/me",
#             response_model=response_schema.ResponseSuccess,
#             tags=[], summary="Change User Me")
# async def read_users_me(new_user_data: user_schema.ChangeUser,
#                         db: Session = Depends(get_db),
#                         current_db_user=Depends(users_crud.get_current_user)):
#     users_crud.change_user_data(user=current_db_user, user_data=new_user_data, db=db)
#     return {"message": "success"}
