from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, model_validator

from app.utils import enums


class AuthDetailBase(BaseModel):
    server_name: str
    auth_type: enums.AuthTypeEnum
    http_method: str
    api_url: str
    username: Optional[str] = Field(None)
    password: Optional[str] = Field(None)
    bearer_token: Optional[str] = Field(None)
    auth_url: Optional[str] = Field(None)
    grant_type: Optional[str] = Field(None)
    client_id: Optional[str] = Field(None)
    client_secret: Optional[str] = Field(None)
    scope: Optional[str] = Field(None)
    created_by: Optional[str] = Field(None, examples=["user"])
    modified_by: Optional[str] = Field(None, examples=["user"])

    @model_validator(mode="after")
    def validate_attributes(self):
        if self.http_method.lower() not in ["get", "post", "put", "patch", "delete"]:
            raise ValueError(
                "invalid HTTP method. Supported types: get/post/put/patch/delete"
            )
        if (
            "spatial" not in self.server_name.lower()
            and "nlyte" not in self.server_name.lower()
            and "comcast" not in self.server_name.lower()
        ):
            raise ValueError(
                "server name should contain term spatial or nlyte or comcast (just for "
                "demo purpose because we dont use any working source endpoints here)"
            )
        if self.auth_type == enums.AuthTypeEnum.BASIC_AUTH and not all(
            [self.username, self.password]
        ):
            raise ValueError("basic auth-type requires username and password")
        elif (
            self.auth_type == enums.AuthTypeEnum.BEARER_TOKEN and not self.bearer_token
        ):
            raise ValueError("bearer_token auth-type requires bearer_token")
        elif self.auth_type == enums.AuthTypeEnum.OAUTH2 and not all(
            [self.auth_url, self.client_id, self.client_secret, self.scope]
        ):
            raise ValueError(
                "oauth2 auth-type requires auth_url, client_id, client_secret and scope"
            )

        return self


class AuthDetailCreate(AuthDetailBase):
    pass


class AuthDetailUpdate(AuthDetailBase):
    pass


class AuthDetailInDb(AuthDetailBase):
    id: int
    api_name: str
    created_at: datetime
    modified_at: datetime

    class Config:
        from_attributes = True
