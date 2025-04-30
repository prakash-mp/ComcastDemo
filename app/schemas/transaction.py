from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime


class TransactionBase(BaseModel):
    tid: str
    order_status: str
    order_type: str
    source_api: Optional[str] = Field(
        None,
        examples=["spatial"],
        description="api name (spatial or nlyte)",
    )
    created_by: Optional[str] = Field(None, examples=["user"])
    modified_by: Optional[str] = Field(None, examples=["user"])


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    pass


class TransactionInDb(TransactionBase):
    created_at: datetime
    modified_at: datetime
    count: int = None
    source_api: Optional[str] = Field(None, exclude=True)

    class Config:
        from_attributes = True
