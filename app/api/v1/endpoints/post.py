from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from app.api.dependencies import get_db
from app.crud import category as category_crud
from app.schemas import response as response_schema, post as post_schema, category as category_schema
from app.schemas.response import custom_errors
from app.utils import image as image_utils, post_additional_fields_validation as add_fields_valid

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("", summary="Add post",
             response_model=response_schema.ResponseSuccess,
             responses={
                 409: custom_errors("Conflict", [{"msg": "Category not exist or not for posting"}]),
                 400: custom_errors("Bad Request", [{"msg": "Not all required fields are filled",
                                                     "blank fields": ["blank_field"]},
                                                    {"msg": "Duplicated additional fields"},
                                                    {"msg": "Additional field validation error",
                                                     "errors": [{"alias": "alias_one",
                                                                 "error": "error_one"}]},
                                                    {"msg": "Post no have images"},
                                                    {"msg": "Image has not been validated",
                                                     "not_verified_images": [
                                                         {"index": 0, "filename": "image_filename"}
                                                     ]}])
                        })
async def add_post(post_data: post_schema.PostCreate = Form(),
                   images: List[UploadFile] = File(None),
                   db: Session = Depends(get_db)):
    category: category_schema.Category = category_crud.get_category_posting_data_by_id(category_id=post_data.categoryId,
                                                                                       db=db)
    if not category:
        raise HTTPException(status_code=409, detail={"msg": "Category not exist or not for posting"})
    blank_fields = add_fields_valid.get_blank_required_fields(post_additional_fields=post_data.additionalFields,
                                                              required_additional_fields=category.additionalFields)
    if len(blank_fields) > 0:
        raise HTTPException(status_code=400, detail={"msg": "Not all required fields are filled",
                                                     "blank fields": blank_fields})
    if not add_fields_valid.check_duplicate_fields(post_additional_fields=post_data.additionalFields):
        raise HTTPException(status_code=400, detail={"msg": "Duplicated additional fields"})
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

    # print(post_data)

    return {"msg": "success"}
