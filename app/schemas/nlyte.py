from pydantic import BaseModel, Field, confloat, model_validator
from typing import Optional
from enum import Enum


class AssetTypeEnum(str, Enum):
    Server = "server"
    Cooling_Unit = "cooling_unit"
    Rack = "rack"


class AssetStatusEnum(str, Enum):
    Active = "active"
    Decommissioned = "decommissioned"


class CoolingUnitStatusEnum(str, Enum):
    Operational = "operational"
    Under_Maintenance = "under_maintenance"


class Location(BaseModel):
    address: Optional[str] = Field(None, examples=["375 Rockbridge Rd NW"])
    latitude: confloat(ge=-90, le=90)
    longitude: confloat(ge=-180, le=180)


class NlyteAsset(BaseModel):
    asset_id: str = Field(examples=["Asset123"])
    asset_type: AssetTypeEnum = Field(
        description="server, cooling unit, rack", examples=["server"]
    )
    manufacturer: str = Field(examples=["Dell"])
    model: str = Field(examples=["PowerEdge R740"])
    asset_status: AssetStatusEnum = Field(
        description="Active/Decommissioned", examples=["active"]
    )
    asset_location: str = Field(
        description="Location within the data center", examples=["Rack 15"]
    )


class NlyteEnergyUsage(BaseModel):
    power_consumption_kw: float = Field(
        description="Power consumption in kilowatts", examples=[10.0]
    )
    peak_usage_kw: float = Field(
        description="Peak power usage in kilowatts", examples=[8.0]
    )
    average_usage_kw: float = Field(
        description="Average power consumption over time in kilowatts", examples=[6.0]
    )
    energy_efficiency_rating: str = Field(description="A+, A, B, etc.", examples=["A"])


class NlyteCooling(BaseModel):
    cooling_capacity_ton: float = Field(
        description="Cooling capacity in tons", examples=[10.0]
    )
    current_temperature_celsius: float = Field(
        description="Current temperature maintained by the cooling unit", examples=[48]
    )
    cooling_unit_status: CoolingUnitStatusEnum = Field(
        description="Operational, Under Maintenance, etc.", examples=["operational"]
    )
    cooling_unit_location: str = Field(
        description="Physical location of the cooling unit", examples=["Rack 17"]
    )


class NlyteBase(BaseModel):
    dc_id: str = Field(examples=["DC1"])
    name: str = Field(examples=["Telecom Data Center 1"])
    location: Location
    power_capacity_kw: float = Field(
        description="total power capacity", examples=[20.0]
    )
    available_power_capacity_kw: float = Field(
        description="Remaining available power capacity", examples=[10.0]
    )
    total_racks: int = Field(description="total rack capacity", examples=[100])
    available_racks: int = Field(description="remaining available rack", examples=[100])
    asset: NlyteAsset
    energy_usage: NlyteEnergyUsage
    cooling_unit: NlyteCooling


class NlyteCreate(NlyteBase):
    pass


class NlyteUpdate(NlyteBase):
    pass


class NlyteInDb(NlyteBase):
    hub_id: str
    tid: Optional[str]
