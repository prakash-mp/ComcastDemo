from pydantic import BaseModel, Field, confloat
from typing import Optional
from enum import Enum


class InfraStatusEnum(str, Enum):
    Operational = "operational"
    Under_Maintenance = "under_maintenance"


class NetworkTypeEnum(str, Enum):
    G4 = "4g"
    G5 = "5g"
    LTE = "lte"


class Location(BaseModel):
    address: Optional[str] = Field(None, examples=["375 Rockbridge Rd NW"])
    latitude: confloat(ge=-90, le=90)
    longitude: confloat(ge=-180, le=180)


class Infrastructure(BaseModel):
    power_capacity_kw: float = Field(examples=[20.0])
    cooling_capacity_ton: float = Field(examples=[10.0])
    infrastructure_type: str = Field(
        description="DataCenter/BaseStation/Tower etc", examples=["data_center"]
    )
    infrastructure_status: InfraStatusEnum = Field(
        description="Operation/UnderMaintenance", examples=[InfraStatusEnum.Operational]
    )
    infrastructure_capacity: Optional[int] = Field(
        None, description="number of connections it can support"
    )


class SpatialSignalPropagation(BaseModel):
    propagation_distance_km: float = Field(
        description="Distance(KM) from the source or base station", examples=[20.0]
    )
    terrain_type: str = Field(
        description="urban, rural, mountainous", examples=["urban"]
    )
    signal_loss_db: float = Field(description="Signal loss in decibels", examples=[2.0])
    interference_level_db: Optional[float] = Field(
        description="Signal loss in decibels", examples=[2.0]
    )


class SpatialNetworkCoverage(BaseModel):
    coverage_area_km2: float = Field(
        description="Area covered by the network in square kilometers", examples=[100.0]
    )
    signal_strength_dbm: float = Field(
        description="Signal strength in dBm", examples=[33.0]
    )
    network_type: str = Field(description="4G, 5G, LTE", examples=[NetworkTypeEnum.LTE])


class SpatialBase(BaseModel):
    name: str = Field(examples=["NYC-Tower1"])
    region: str = Field(examples=["Manhattan Tower"])
    location: Location
    infrastructure: Infrastructure
    signal_propagation: SpatialSignalPropagation
    network_coverage: SpatialNetworkCoverage


class SpatialCreate(SpatialBase):
    pass


class SpatialUpdate(SpatialBase):
    pass


class SpatialInDb(SpatialBase):
    hub_id: str
    tid: Optional[str]
