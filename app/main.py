from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.db.session import engine
# from app.db.db_models import Base
from app.api.v1.aggregator import api_router
from app.core.config import settings

# Base.metadata.create_all(bind=engine)

app = FastAPI(
    root_path=settings.ROOT_PATCH,
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    contact=settings.CONTACTS,
    openapi_tags=settings.OPENAPI_TAGS
)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
