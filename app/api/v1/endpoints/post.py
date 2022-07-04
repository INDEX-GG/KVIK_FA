from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.dependencies import get_db
from app.crud import category as category_crud
from app.schemas import response as response_schema, category as category_schema

router = APIRouter(prefix="/posts", tags=["Categories"])


@router.get("/",
            # response_model=category_schema.CategoryAdditionalFields,
            tags=[], summary="Add post",
            # responses={409: response_schema.custom_errors("Conflict", ["Category not exist or not for posting"])}
            )
async def start(db: Session = Depends(get_db)):
    return "HELLOU"
