from fastapi import APIRouter, Depends, HTTPException, responses
from uuid import UUID
from sqlalchemy.orm import Session
from pathlib import Path
from app.api.dependencies import get_db
from app.crud import image as image_crud
from app.schemas import post as post_schema


router = APIRouter(prefix="/images", tags=["Images"])


@router.get("/{resolution}/{image_uuid}", summary="Get Image By UUID", response_class=responses.FileResponse)
async def get_image(resolution: post_schema.PostImageResolutions, image_uuid: UUID, db: Session = Depends(get_db)):
    db_photo = image_crud.get_image_by_uuid(db=db, image_uuid=image_uuid)
    if not db_photo:
        raise HTTPException(404)
    image = f"./files{db_photo.road}/{resolution.value}.webp"
    if not Path(image).is_file():
        raise HTTPException(404)
    return image
