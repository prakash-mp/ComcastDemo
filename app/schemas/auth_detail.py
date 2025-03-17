from typing import Optional

from pydantic import BaseModel, Field, model_validator

from app.utils import enums


class AuthDetailBase(BaseModel):
    auth_type: enums.AuthTypeEnum
    username: Optional[str] = Field(None)
    password: Optional[str] = Field(None)
    bearer_token: Optional[str] = Field(None)
    auth_url: Optional[str] = Field(None)
    client_id: Optional[str] = Field(None)
    client_secret: Optional[str] = Field(None)
    scope: Optional[str] = Field(None)

    @model_validator(mode="after")
    def validate_attributes(self):
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

    class Config:
        from_attributes = True
