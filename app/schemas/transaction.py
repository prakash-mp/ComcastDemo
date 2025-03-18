from typing import Optional

from pydantic import BaseModel, Field
from datetime import datetime


class TransactionBase(BaseModel):
    tid: str
    order_status: str
    created_by: Optional[str] = Field(None, examples=["user"])
    modified_by: Optional[str] = Field(None, examples=["user"])


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    pass


class TransactionInDb(TransactionBase):
    created_at: datetime
    modified_at: datetime

    class Config:
        from_attributes = True
