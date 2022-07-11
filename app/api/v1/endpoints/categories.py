from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api.dependencies import get_db
from app.crud import category as category_crud
from app.schemas import category as category_schema
from app.schemas.response import custom_errors
from app.utils import post_additional_fields_validation as add_fields_valid


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/{category_id}/additional_fields", summary="Get Category Additional fields",
            response_model=category_schema.Category,
            responses={
                409: custom_errors("Conflict", [{"msg": "Category not exist or not for posting"}])
                       })
async def get_category_add_fields(category_id,
                                  db: Session = Depends(get_db)):
    category: category_schema.Category = category_crud.get_category_posting_data_by_id(category_id=category_id, db=db)
    if not category:
        raise HTTPException(status_code=409, detail={"msg": "Category not exist or not for posting"})
    return category.__dict__


@router.get("/additional_fields/yearly_quarter_hint", summary="Get Yearly Quarter Hint",
            response_model=List[str]
            )
async def get_yearly_quarter_hint():
    return add_fields_valid.get_yearly_quarters()
