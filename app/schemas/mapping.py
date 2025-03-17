from pydantic import BaseModel, Field
from typing import List, Optional


class Rule(BaseModel):
    source: str
    destination: str
    optional: Optional[str] = Field(None)


class MappingBase(BaseModel):
    mapping_profile: str
    rule: List[Rule]


class MappingCreate(MappingBase):
    pass


class MappingUpdate(MappingBase):
    pass


class MappingInDb(MappingBase):
    class Config:
        from_attributes = True
