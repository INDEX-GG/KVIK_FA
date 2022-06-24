import unittest
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.api.v1.aggregator import api_router
from app.core.config import settings
from app.db.db_models import Base


def start_application():
    app = FastAPI(
        root_path=settings.ROOT_PATCH,
        title=settings.TITLE,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
        contact=settings.CONTACTS,
        openapi_tags=settings.OPENAPI_TAGS
    )
    app.include_router(api_router)
    return app


SQLALCHEMY_DATABASE_URL = settings.TESTS_SQLALCHEMY_DATABASE_URL
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
Base.metadata.drop_all(bind=engine)


class Test(unittest.TestCase):
    def test_square(self):
        self.assertEquals(4, 4)
