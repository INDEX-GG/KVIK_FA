from sqlalchemy.orm import Session
from app.db.db_models import PostPhoto
from uuid import UUID


def get_image_by_uuid(db: Session, image_uuid: UUID):
    db_image = db.query(PostPhoto).filter(PostPhoto.uuid == image_uuid).first()
    if db_image:
        return db_image
    else:
        return False
