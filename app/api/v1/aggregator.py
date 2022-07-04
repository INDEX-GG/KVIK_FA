from fastapi import APIRouter

from app.api.v1.endpoints import users, phone, login, posts

api_router = APIRouter(prefix="/v1")
api_router.include_router(users.router)
api_router.include_router(phone.router)
api_router.include_router(login.router)
api_router.include_router(posts.router)