from sqlalchemy.orm import Session
from app.db.db_models import PostingCategories


def get_category_posting_data_by_id(db: Session, category_id: int):
    db_category_posting_data = db.query(PostingCategories).filter(PostingCategories.id == category_id).first()
    if db_category_posting_data:
        return db_category_posting_data
    else:
        return False
