from pydantic import BaseModel


def custom_errors(description: str, error_list: list):
    errors_dict = {"description": description, "content": {"application/json": {"examples": {}}}}
    for err in error_list:
        errors_dict["content"]["application/json"]["examples"][err] = {"summary": err, "value": {"detail": err}}
    print(errors_dict)
    return errors_dict


class ResponseSuccess(BaseModel):
    message: str = "success"


class ResponseCustomError(BaseModel):
    detail: str


class ResponseLogin(BaseModel):
    refreshToken: str
    accessToken: str
    tokenType: str
