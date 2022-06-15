from pydantic import BaseModel


class ResponseSuccess(BaseModel):
    message: str = "success"


class ResponseCustomError(BaseModel):
    detail: str


class ResponseLogin(BaseModel):
    refreshToken: str
    accessToken: str
    tokenType: str
