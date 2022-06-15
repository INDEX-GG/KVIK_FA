from fastapi import APIRouter


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/123")
async def read_users_me():
    return "321"
