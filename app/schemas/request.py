from pydantic import BaseModel, constr


class RequestGoogleData(BaseModel):
    token: str


class VkDataDict(BaseModel):
    uid: int
    first_name: str
    last_name: str
    photo: str
    hash: str


class RequestVkData(BaseModel):
    auth_data: VkDataDict


class RequestAppleData(BaseModel):
    id_token: str
    email: str | None = None
    firstName: str | None = "Anonim"
    lastName: str | None = None
