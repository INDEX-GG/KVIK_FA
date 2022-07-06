from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.api.dependencies import get_db
from app.crud import category as category_crud, post as post_crud
from app.schemas import response as response_schema, post as post_schema, category as category_schema
from app.schemas.response import custom_errors
from app.utils import image as image_utils


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("", summary="Add post",
             response_model=response_schema.ResponseSuccess,
             responses={
                 409: custom_errors("Conflict", [{"msg": "Category not exist or not for posting"}]),
                 400: custom_errors("Bad Request", [{"msg": "Not all required fields are filled",
                                                     "blank fields": ["blank_field"]},
                                                    {"msg": "Duplicated additional fields"},
                                                    {"msg": "Post no have images"},
                                                    {"msg": "Image has not been validated"}])
                        })
async def start(post_data: post_schema.PostCreate = Form(),
                images: List[UploadFile] = File(None),
                db: Session = Depends(get_db)):
    category: category_schema.Category = category_crud.get_category_posting_data_by_id(category_id=post_data.categoryId,
                                                                                       db=db)
    if not category:
        raise HTTPException(status_code=409, detail={"msg": "Category not exist or not for posting"})
    blank_fields = post_crud.get_blank_required_fields(post_additional_fields=post_data.additionalFields,
                                                       required_additional_fields=category.additionalFields)
    if len(blank_fields) > 0:
        raise HTTPException(status_code=400, detail={"msg": "Not all required fields are filled",
                                                     "blank fields": blank_fields})
    if not post_crud.check_duplicate_fields(post_additional_fields=post_data.additionalFields):
        raise HTTPException(status_code=400, detail={"msg": "Duplicated additional fields"})
    if not images:
        raise HTTPException(status_code=400, detail={"msg": "Post no have images"})
    not_verified_images = image_utils.checking_images_for_validity(images)
    if len(not_verified_images) > 0:
        raise HTTPException(status_code=400, detail={"msg": "Image has not been validated",
                                                     "not_verified_images": not_verified_images})

    print(post_data)

    return {"msg": "success"}
