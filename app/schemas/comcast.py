from pydantic import BaseModel, Field, confloat, validator
from typing import List, Union, Optional, Any
from enum import Enum


class HubTypeEnum(str, Enum):
    Primary = "primary"
    Secondary = "secondary"


class Location(BaseModel):
    type: str = Field(examples=["Point"])
    coordinates: List[float] = Field(examples=[[-84.16322687, 33.88408157]])

    @validator("coordinates", pre=True)
    def coordinate_validator(cls, value):
        if isinstance(value, str):
            value = value.split(", ")

        if len(value) != 2:
            raise ValueError("inValid Co-ordinates")

        long, lat = float(value[0]), float(value[1])

        if not (-180 <= long <= 180):
            raise ValueError("Invalid longitude")

        if not (-90 <= lat <= 90):
            raise ValueError("Invalid latitude")

        return value


class Hub(BaseModel):
    hubCode: str = Field(examples=["GAL1"])
    hubName: str = Field(examples=["Aurora.CO"])
    hubType: HubTypeEnum = Field(examples=["primary"])
    primaryHubId: str = Field(examples=["5ede4d9cf41a0058f1949bbe"])
    addr1: str = Field(examples=["375 Rockbridge Rd NW"])
    addr2: Optional[str] = Field(None, examples=["Unit 2"])
    city: str = Field(examples=["LILBURN"])
    BuhmId: str = Field(examples=["5ede4d9cf41a0058f1949bbe"])
    countryCode: str = Field(examples=["CAN"])
    locality: str = Field(examples=["locality"])
    serviceStatus: str = Field(examples=["I"])
    state: str = Field(examples=["GA"])
    zipCode: str = Field(examples=["30047"])
    timezone: str = Field(examples=["EST"])
    location: Location

    @validator("zipCode", pre=True)
    def check_zip_code(cls, value):
        if isinstance(value, float):
            value = str(int(value))
        return value


class ComcastBase(BaseModel):
    partner: Union[List[str], str] = Field(default=["comcast", "rogers"])
    hub_id: str = Field(examples=["5ede4d9cf41a0058f1949bbe"])
    hub: Hub
    createdBy: Optional[str] = Field(None, examples=["user"])
    modifiedBy: Optional[str] = Field(None, examples=["user"])

    @validator("partner")
    def partner_formatter(cls, value):
        if isinstance(value, str):
            value = value.split(", ")

        return value


class ComcastCreate(ComcastBase):
    pass


class ComcastUpdate(ComcastBase):
    pass


class ComcastInDb(ComcastBase):
    tid: Optional[str]
