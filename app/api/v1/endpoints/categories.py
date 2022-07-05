from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.crud import category as category_crud
from app.schemas import category as category_schema
from app.schemas.response import custom_errors


router = APIRouter(prefix="/categories", tags=["Posts"])


@router.get("/{category_id}/additional_fields", summary="Get Category Additional fields",
            response_model=category_schema.CategoryAdditionalFields,
            responses={
                409: custom_errors("Conflict", [{"msg": "Category not exist or not for posting"}])
                       })
async def start(category_id,
                db: Session = Depends(get_db)):
    category = category_crud.get_category_posting_data_by_id(category_id=category_id, db=db)
    if not category:
        raise HTTPException(status_code=409, detail={"msg": "Category not exist or not for posting"})
    additional_fields = category.additionalFields
    return additional_fields
