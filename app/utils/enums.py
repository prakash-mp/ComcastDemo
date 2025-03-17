from enum import Enum


class AuthTypeEnum(str, Enum):
    BASIC_AUTH = "basic_auth"
    BEARER_TOKEN = "bearer_token"
    OAUTH2 = "oauth2"
