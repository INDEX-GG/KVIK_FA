from PIL import Image, UnidentifiedImageError
from fastapi import APIRouter, Depends, File, HTTPException
from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, FileResponse
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.crud import post as post_crud
from app.crud import user as users_crud
from app.schemas import post as post_schema

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("", summary="Uploading a post",
             description="", include_in_schema=True)
async def create_post(post_data: post_schema.PostCreateRequest,
                      user=Depends(users_crud.get_current_user),
                      db: Session = Depends(get_db)
                      ):
    """Create a new post from user input.

        Keyword arguments:
        post_data -- user input inside a Basemodel class
        user -- user profile (Basemodel class)
        db -- database connection

    """
    user_id = int(user.id)
    post_crud.create_post(post=post_data, db=db, user_id_out=user_id)
    return {"message": "success"}


@router.post("/upload_photo")
async def create_upload_file(post_id: int,
                             file: UploadFile = File(),
                             db: Session = Depends(get_db),
                             user=Depends(users_crud.get_current_user)
                             ):
    """Upload photo and add it to existing post.

       Keyword arguments:
       post_id -- unique post identifier received from query
       file -- object received via formdata
       db -- database connection
       user -- user profile (Basemodel class)

    """
    post_edited = post_crud.get_post_out(db=db, post_id=post_id)
    if post_edited.userId == user.id:
        try:
            im = Image.open(file.file)
            filename = post_crud.save_photo(file=file, im=im)
            im.close()
            post_crud.create_file_record(db=db, post_id=post_id, url=filename)
            return {"Result": "OK"}
        except UnidentifiedImageError:
            return {"Result": "Failed"}
    else:
        raise HTTPException(status_code=401, detail='Not Authorized for editing this post')


@router.post("/mod", summary="Blocking a post by moderator",
             description="")
async def block_post_mod(post_id: int,
                         db: Session = Depends(get_db),
                         user=Depends(users_crud.get_current_user)
                         ):
    """Create a record of a post blocked by a moderator.

      Keyword arguments:
      post_id -- unique post identifier received from query
      db -- database connection
      user -- user profile (Basemodel class)

    """
    user_id = int(user.id)
    new_block = post_crud.create_block_mod(db=db, user_id=user_id, post_id=post_id)
    if new_block:
        return {"message": "success"}
    else:
        return {"message": "failure"}


@router.put("/{post_id}", summary="Editing a post",
            description="")
async def edit_post(post_id: int,
                    post_data: post_schema.PostEditRequest,
                    db: Session = Depends(get_db),
                    user=Depends(users_crud.get_current_user)
                    ):
    """Replace the post attributes with ones received via user input.

       Keyword arguments:
       post_id -- unique post identifier received from path
       post_data -- user input inside a Basemodel class
       db -- database connection
       user -- user profile (Basemodel class)

    """
    post_edited = post_crud.get_post_out(db=db, post_id=post_id)
    if post_edited.userId == user.id:
        edit = post_crud.update_post(db=db, post_data=post_data, post_id=post_id)
        if edit:
            return {"message": "Post edited successfully"}
        else:
            return {"message": "No changes applied"}
    else:
        raise HTTPException(status_code=401, detail='Not Authorized for editing this post')


@router.get("/{post_id}", summary="Viewing a particular post",
            description="")
async def view_post(post_id: int,
                    db: Session = Depends(get_db)
                    ):
    """Return a post with an id given.

       Keyword arguments:
       post_id -- unique post identifier received from path
       db -- database connection

    """
    post_edited: dict = post_crud.get_post_view(db=db, post_id=post_id)
    post_edited = jsonable_encoder(post_edited)
    return JSONResponse(content=[post_edited])


@router.get("/{post_id}/{photo_id}", summary="Viewing a photo of a particular post",
            description="")
async def view_post(post_id: int,
                    photo_id: int,
                    db: Session = Depends(get_db)
                    ):
    """Return a photo from a post with an id given.

       Keyword arguments:
       post_id -- unique post identifier received from path
       photo_id -- unique image identifier received from path
       db -- database connection

    """
    file_name: str = post_crud.get_file_out(db=db, post_id=post_id, photo_id=photo_id)
    path_rel = post_crud.get_file_path(file_name=file_name)
    return FileResponse(path=path_rel)


@router.get("", summary="Viewing all posts",
            description="")
async def view_posts(db: Session = Depends(get_db),
                     user=Depends(users_crud.get_current_user)
                     ):
    """Return all posts, except ones blocked either user or moderator.

       Keyword arguments:
       db -- database connection
       user -- user profile (Basemodel class)

    """
    user_id = int(user.id)
    post_edited: dict = post_crud.get_post_view_all(db=db, user_id=user_id)
    post_edited = jsonable_encoder(post_edited)
    return JSONResponse(content=[post_edited])


@router.post("/block", summary="Blocking a particular post for yourself",
             description="")
async def block_post_pers(post_id: int,
                          db: Session = Depends(get_db),
                          user=Depends(users_crud.get_current_user)
                          ):
    """Create a record of a post blocked by a user logged in.

          Keyword arguments:
          post_id -- unique post identifier received from query
          db -- database connection
          user -- user profile (Basemodel class)

        """
    user_id = int(user.id)
    post_block = post_crud.get_post_out(db=db, post_id=post_id)
    if post_block.userId == user.id:
        new_block = post_crud.create_block_pers(db=db, user_id=user_id, post_id=post_id)
        if new_block:
            return {"message": "success"}
        else:
            return {"message": "failure"}
