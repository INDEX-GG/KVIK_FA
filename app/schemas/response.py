from pydantic import BaseModel


def custom_errors(description: str, error_list: list):
    errors_dict = {"description": description, "content": {"application/json": {"examples": {}}}}
    for err in error_list:
        errors_dict["content"]["application/json"]["examples"][err["msg"]] = {"summary": err["msg"], "value": err}
    return errors_dict


class ResponseSuccess(BaseModel):
    msg: str = "success"


class ResponseSuccessWithPostId(BaseModel):
    msg: str = "success"
    postId: int


class ResponseCustomError(BaseModel):
    detail: str


class ResponseCheckVerifCode(BaseModel):
    phone_token: str


class ResponseCheckPhoneRegistration(BaseModel):
    phoneRegistration: bool


class ResponseLogin(BaseModel):
    refreshToken: str
    accessToken: str


class AccessToken(BaseModel):
    accessToken: str
