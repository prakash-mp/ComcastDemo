from pydantic import BaseModel
from datetime import datetime


class TransactionBase(BaseModel):
    order_id: str
    submitted_by: str
    order_status: str


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    pass


class TransactionInDb(TransactionBase):
    created_at: datetime

    class Config:
        from_attributes = True
