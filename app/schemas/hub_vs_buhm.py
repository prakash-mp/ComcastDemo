from pydantic import BaseModel, Field


class HubVsBuhmBase(BaseModel):
    hub_id: str
    BuhmId: str


class HubVsBuhmCreate(HubVsBuhmBase):
    pass


class HubVsBuhmUpdate(HubVsBuhmBase):
    pass


class HubVsBuhmInDb(HubVsBuhmBase):
    class Config:
        from_attributes = True
