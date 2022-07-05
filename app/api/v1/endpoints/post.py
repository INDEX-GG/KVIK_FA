from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.crud import category as category_crud
from app.schemas import response as response_schema, post as post_schema
from app.schemas.response import custom_errors


router = APIRouter(prefix="/posts", tags=["Categories"])


@router.post("", summary="Add post",
             response_model=response_schema.ResponseSuccess,
             responses={
                 409: custom_errors("Conflict", [{"msg": "Category not exist or not for posting"}]),
                 400: custom_errors("Bad Request", [{"msg": "Not all required fields are filled",
                                                     "blank fields": ["blank_field"]}])
                        })
async def start(post_data: post_schema.PostCreate,
                db: Session = Depends(get_db)):
    category = category_crud.get_category_posting_data_by_id(category_id=post_data.categoryId, db=db)
    if not category:
        raise HTTPException(status_code=409, detail={"msg": "Category not exist or not for posting"})
    additional_fields = category.additionalFields

    required_additional_fields_aliases = set(x["alias"] for x in additional_fields if x["requiring"] is True)
    post_additional_fields = set(x.alias for x in list(post_data.additionalFields) if x.value is not None)
    blank_fields = list(required_additional_fields_aliases - post_additional_fields)
    if len(blank_fields) != 0:
        raise HTTPException(status_code=400, detail={"msg": "Not all required fields are filled",
                                                     "blank fields": blank_fields})


    print()
    print(post_data)

    return {"message": "success"}
