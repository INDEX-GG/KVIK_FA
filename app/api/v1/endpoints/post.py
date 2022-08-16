from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File, BackgroundTasks, Body
from sqlalchemy.orm import Session
from typing import List
from app.api.dependencies import get_db
from app.crud import category as category_crud, post as post_crud, user as users_crud
from app.schemas import response as response_schema, post as post_schema, category as category_schema, \
    user as user_schema
from app.schemas.response import custom_errors
from app.utils import image as image_utils, post_additional_fields_validation as add_fields_valid

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("", summary="Add Post",
             response_model=response_schema.ResponseSuccessWithPostId, status_code=201,
             responses={
                 500: custom_errors("Server Error", [{"msg": "Image loading error"}]),
                 409: custom_errors("Conflict", [{"msg": "Category not exist or not for posting"}]),
                 400: custom_errors("Bad Request", [{"msg": "Not all required fields are filled",
                                                     "blankFields": ["blank_field"]},
                                                    {"msg": "Duplicated additional fields"},
                                                    {"msg": "Category require post title"},
                                                    {"msg": "Additional field validation error",
                                                     "errors": [{"alias": "alias_one",
                                                                 "error": "error_one"}]},
                                                    {"msg": "Post no have images"},
                                                    {"msg": "Image has not been validated",
                                                     "not_verified_images": [
                                                         {"index": 0, "filename": "image_filename"}
                                                     ]}])
                        })
async def add_post(background_tasks: BackgroundTasks,
                   post_data: post_schema.PostCreate = Form(),
                   images: List[UploadFile] = File(None),
                   current_user: user_schema.UserOut = Depends(users_crud.get_current_user),
                   db: Session = Depends(get_db)):

    category: category_schema.Category = category_crud.get_category_posting_data_by_id(category_id=post_data.categoryId,
                                                                                       db=db)
    if not category:
        raise HTTPException(status_code=409, detail={"msg": "Category not exist or not for posting"})

    if post_data.title is None:
        raise HTTPException(status_code=400, detail={"msg": "require title"})

    # if category.dynamicTitle is False and post_data.title is None:
    #     raise HTTPException(status_code=400, detail={"msg": "Category require post title"})
    # if category.dynamicTitle is True:
    #     post_data.title = post_crud.create_dynamic_title(category=category)

    post_additional_fields = add_fields_valid.get_post_additional_fields(
        post_additional_fields=post_data.additionalFields,
        required_additional_fields=category.additionalFields)
    blank_fields = add_fields_valid.get_blank_required_fields(post_additional_fields=post_additional_fields,
                                                              required_additional_fields=category.additionalFields)
    if len(blank_fields) > 0:
        raise HTTPException(status_code=400, detail={"msg": "Not all required fields are filled",
                                                     "blankFields": blank_fields})
    add_fields_valid_err = \
        add_fields_valid.validate_additional_fields(post_additional_fields=post_data.additionalFields,
                                                    additional_fields_schema=category.additionalFields)
    if len(add_fields_valid_err) > 0:
        raise HTTPException(status_code=400, detail={"msg": "Additional field validation error",
                                                     "errors": add_fields_valid_err})
    if not images:
        raise HTTPException(status_code=400, detail={"msg": "Post no have images"})
    not_verified_images = image_utils.checking_images_for_validity(images)
    if len(not_verified_images) > 0:
        raise HTTPException(status_code=400, detail={"msg": "Image has not been validated",
                                                     "not_verified_images": not_verified_images})

    db_post = post_crud.create_post(db=db, post=post_data,
                                    post_additional_fields=post_additional_fields,
                                    user=current_user)

    background_tasks.add_task(image_utils.save_images, images=images, post_id=db_post.id, db=db)
    return {"msg": "success", "postId": db_post.id}


@router.put("/{post_id}", summary="Edit Post By Id",
            response_model=response_schema.ResponseSuccess, status_code=200,
            responses={
                500: custom_errors("Server Error", [{"msg": "Image loading error"}]),
                400: custom_errors("Bad Request", [{"msg": "Duplicated additional fields"},
                                                   {"msg": "Additional fields not for edit",
                                                    "not_for_edit_fields": ["not_for_edit_field"]},
                                                   {"msg": "Additional field validation error",
                                                    "errors": [{"alias": "alias_one",
                                                                "error": "error_one"}]},
                                                   {"msg": "Image has not been validated",
                                                    "not_verified_images": [
                                                        {"index": 0, "filename": "image_filename"}
                                                    ]}])
                        })
async def edit_post(background_tasks: BackgroundTasks,
                    post_id: int,
                    post_data: post_schema.PostEdit = Form(),
                    images: List[UploadFile | int] = File([]),
                    current_user: user_schema.UserOut = Depends(users_crud.get_current_user),
                    db: Session = Depends(get_db)):

    db_post = post_crud.get_user_post_by_id(db=db, post_id=post_id, user_id=current_user.id)
    if not db_post:
        raise HTTPException(404)
    category: category_schema.Category = category_crud.get_category_posting_data_by_id(category_id=db_post.categoryId,
                                                                                       db=db)
    if not category:
        raise HTTPException(status_code=409, detail={"msg": "Category not exist or not for posting"})

    post_additional_fields = add_fields_valid.get_post_additional_fields(
        post_additional_fields=post_data.additionalFields,
        required_additional_fields=category.additionalFields)

    not_for_edit_fields = add_fields_valid.get_not_for_edit_fields(post_additional_fields=post_additional_fields,
                                                                   required_additional_fields=category.additionalFields)
    if len(not_for_edit_fields) > 0:
        raise HTTPException(status_code=400, detail={"msg": "Additional fields not for edit",
                                                     "not_for_edit_fields": not_for_edit_fields})
    add_fields_valid_err = \
        add_fields_valid.validate_additional_fields(post_additional_fields=post_additional_fields,
                                                    additional_fields_schema=category.additionalFields)
    if len(add_fields_valid_err) > 0:
        raise HTTPException(status_code=400, detail={"msg": "Additional field validation error",
                                                     "errors": add_fields_valid_err})

    image_utils.validate_updated_images(images=images, db_post=db_post)

    edited_additional_fields = post_crud.get_edited_additional_fields(edited_fields=post_data.additionalFields,
                                                                      post=db_post)
    post_crud.edit_post(db=db, db_post=db_post, edited_additional_fields=edited_additional_fields, post_data=post_data)

    background_tasks.add_task(image_utils.update_images, images=images, db_post=db_post, db=db)
    return {"msg": "success"}


@router.get("/{post_id}", summary="Get Post By Id",
            response_model=post_schema.PostInDetailOut)
async def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    db_post = post_crud.get_post_by_id(db=db, post_id=post_id)
    if not db_post:
        raise HTTPException(404)
    category: category_schema.Category = category_crud.get_category_posting_data_by_id(category_id=db_post.categoryId,
                                                                                       db=db)
    if not category:
        raise HTTPException(status_code=409, detail={"msg": "Category not exist or not for posting"})
    post_out = post_crud.get_post_in_detail_out(db_post=db_post, category=category)
    return post_out


@router.get("", summary="Get Posts",
            response_model=List[post_schema.PostLiteOut])
async def get_posts(params: post_schema.PostsQuery = Depends(),
                    db: Session = Depends(get_db)):
    db_posts = post_crud.get_posts(db=db, params=params)
    posts_out = post_crud.get_posts_out(db_posts)
    return posts_out


@router.post("/filter", summary="Get Posts With Filters",
             response_model=List[post_schema.PostLiteOut])
async def get_posts(params: post_schema.PostsQuery = Depends(),
                    body: post_schema.PostsFilter = Body(),
                    db: Session = Depends(get_db)):
    db_posts = post_crud.get_posts_with_filters(db=db, params=params, body=body)
    posts_out = post_crud.get_posts_out(db_posts)
    return posts_out
