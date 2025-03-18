from datetime import datetime

from pydantic import BaseModel, Field
from typing import List, Optional


class Rule(BaseModel):
    source: str
    destination: str
    optional: Optional[str] = Field(None)


class MappingBase(BaseModel):
    rule: List[Rule]
    created_by: Optional[str] = Field(None, examples=["user"])
    modified_by: Optional[str] = Field(None, examples=["user"])


class MappingCreate(MappingBase):
    pass


class MappingUpdate(MappingBase):
    pass


class MappingInDb(MappingBase):
    mapping_profile: str
    server_name: str
    created_at: datetime
    modified_at: datetime

    class Config:
        from_attributes = True
