from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.crud import post as post_crud
from app.crud import user as users_crud
# from app.schemas import post as post_schema, response as response_schema
from app.schemas import post as post_schema
from app.db.db_models import User, UserPhoto
from app.schemas import user as user_schema
from app.utils import security

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("", summary="Uploading a post",
             description="")
async def create_post(post_data: post_schema.PostCreateRequest,
                      user=Depends(users_crud.get_current_user),
                      db: Session = Depends(get_db)):
    user_id = int(user.id)
    new_post = post_crud.create_post(post=post_data, db=db, user_id_out=user_id)
    return {"message": "success"}

# router.get("me", response_model=user_schema.UserOut, tags=[], summary="Get Current User")
# async def read_users_me(current_user: dict = Depends(users_crud.get_current_user)):
#     return current_user
