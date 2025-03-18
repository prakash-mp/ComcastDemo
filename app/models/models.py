from typing import Union

from sqlalchemy import Column, Integer, String, Text, Float, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from app import schemas
from app.database.session import Base


class Comcast(Base):
    __tablename__ = "comcast"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, default=None)
    hub_id = Column(String(length=250), nullable=False)
    partner = Column(String(length=250), nullable=False)
    hubCode = Column(String(length=250), nullable=False)
    hubName = Column(String(length=250), nullable=False)
    hubType = Column(String(length=250), nullable=False)
    primaryHubId = Column(String(length=250), nullable=False)
    addr1 = Column(Text(), nullable=False)
    addr2 = Column(Text(), nullable=True)
    city = Column(String(length=250), nullable=False)
    BuhmId = Column(String(length=250), nullable=False)
    countryCode = Column(String(length=250), nullable=False)
    locality = Column(String(length=250), nullable=False)
    serviceStatus = Column(String(length=250), nullable=False)
    state = Column(String(length=250), nullable=False)
    zipCode = Column(String(length=250), nullable=False)
    timezone = Column(String(length=250), nullable=False)
    location_type = Column(String(length=250), nullable=False)
    coordinates = Column(String(length=250), nullable=False)
    createdBy = Column(String(length=250), nullable=True)
    modifiedBy = Column(String(length=250), nullable=True)

    # Reference to order_id in the Transaction table
    tid = Column(String(length=250), ForeignKey("transaction.tid"), nullable=True)

    # Define the relationship with Transaction based on order_id
    transaction = relationship("Transaction", back_populates="comcasts")

    @classmethod
    def from_schema(cls, schema: Union[schemas.ComcastCreate, schemas.ComcastUpdate]):
        return cls(
            hub_id=schema.hub_id,
            partner=", ".join(schema.partner),
            hubCode=schema.hub.hubCode,
            hubName=schema.hub.hubName,
            hubType=schema.hub.hubType,
            primaryHubId=schema.hub.primaryHubId,
            addr1=schema.hub.addr1,
            addr2=schema.hub.addr2,
            city=schema.hub.city,
            BuhmId=schema.hub.BuhmId,
            countryCode=schema.hub.countryCode,
            locality=schema.hub.locality,
            serviceStatus=schema.hub.serviceStatus,
            state=schema.hub.state,
            zipCode=schema.hub.zipCode,
            timezone=schema.hub.timezone,
            location_type=schema.hub.location.type,
            coordinates=", ".join(
                [str(tmp) for tmp in schema.hub.location.coordinates]
            ),  # long, lat
            createdBy=schema.createdBy,
            modifiedBy=schema.modifiedBy,
        )

    def to_schema(self):
        data = {
            "hub_id": self.hub_id,
            "tid": self.tid,
            "partner": self.partner,
            "hub": {
                "hubCode": self.hubCode,
                "hubName": self.hubName,
                "hubType": self.hubType,
                "primaryHubId": self.primaryHubId,
                "addr1": self.addr1,
                "addr2": self.addr2,
                "city": self.city,
                "BuhmId": self.BuhmId,
                "countryCode": self.countryCode,
                "locality": self.locality,
                "serviceStatus": self.serviceStatus,
                "state": self.state,
                "zipCode": self.zipCode,
                "timezone": self.timezone,
                "location": {
                    "type": self.location_type,
                    "coordinates": self.coordinates,
                },
            },
            "createdBy": self.createdBy,
            "modifiedBy": self.modifiedBy,
        }
        return schemas.ComcastInDb(**data)


class Spatial(Base):
    __tablename__ = "spatial"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, default=None)
    hub_id = Column(String(length=250), nullable=False)
    name = Column(String(length=250), nullable=False)
    region = Column(String(length=250), nullable=False)
    address = Column(String(length=250), nullable=True)
    latitude = Column(String(length=250), nullable=False)
    longitude = Column(String(length=250), nullable=False)
    power_capacity_kw = Column(Float, nullable=False)
    cooling_capacity_ton = Column(Float, nullable=False)
    infrastructure_type = Column(String(length=250), nullable=False)
    infrastructure_status = Column(String(length=250), nullable=False)
    infrastructure_capacity = Column(Integer, nullable=True)
    propagation_distance_km = Column(Float, nullable=False)
    terrain_type = Column(String(length=250), nullable=False)
    signal_loss_db = Column(Float, nullable=False)
    interference_level_db = Column(Float, nullable=True)
    coverage_area_km2 = Column(Float, nullable=False)
    signal_strength_dbm = Column(Float, nullable=False)
    network_type = Column(String(length=250), nullable=False)

    # Reference to order_id in the Transaction table
    tid = Column(String(length=250), ForeignKey("transaction.tid"), nullable=True)

    # Define the relationship with Transaction based on order_id
    transaction = relationship("Transaction", back_populates="spatials")

    @classmethod
    def from_schema(
        cls, schema: Union[schemas.SpatialCreate, schemas.SpatialUpdate], hub_id: str
    ):
        return cls(
            hub_id=hub_id,
            name=schema.name,
            region=schema.region,
            address=schema.location.address,
            latitude=schema.location.latitude,
            longitude=schema.location.longitude,
            power_capacity_kw=schema.infrastructure.power_capacity_kw,
            cooling_capacity_ton=schema.infrastructure.cooling_capacity_ton,
            infrastructure_type=schema.infrastructure.infrastructure_type,
            infrastructure_status=schema.infrastructure.infrastructure_status,
            infrastructure_capacity=schema.infrastructure.infrastructure_capacity,
            propagation_distance_km=schema.signal_propagation.propagation_distance_km,
            terrain_type=schema.signal_propagation.terrain_type,
            signal_loss_db=schema.signal_propagation.signal_loss_db,
            interference_level_db=schema.signal_propagation.interference_level_db,
            coverage_area_km2=schema.network_coverage.coverage_area_km2,
            signal_strength_dbm=schema.network_coverage.signal_strength_dbm,
            network_type=schema.network_coverage.network_type,
        )

    def to_schema(self):
        data = {
            "hub_id": self.hub_id,
            "tid": self.tid,
            "name": self.name,
            "region": self.region,
            "location": {
                "address": self.address,
                "latitude": self.latitude,
                "longitude": self.longitude,
            },
            "infrastructure": {
                "power_capacity_kw": self.power_capacity_kw,
                "cooling_capacity_ton": self.cooling_capacity_ton,
                "infrastructure_type": self.infrastructure_type,
                "infrastructure_status": self.infrastructure_status,
                "infrastructure_capacity": self.infrastructure_capacity,
            },
            "signal_propagation": {
                "propagation_distance_km": self.propagation_distance_km,
                "terrain_type": self.terrain_type,
                "signal_loss_db": self.signal_loss_db,
                "interference_level_db": self.interference_level_db,
            },
            "network_coverage": {
                "coverage_area_km2": self.coverage_area_km2,
                "signal_strength_dbm": self.signal_strength_dbm,
                "network_type": self.network_type,
            },
        }
        return schemas.SpatialInDb(**data)


class Nlyte(Base):
    __tablename__ = "nlyte"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, default=None)
    hub_id = Column(String(length=250), nullable=False)
    dc_id = Column(String(length=250), nullable=False)
    name = Column(String(length=250), nullable=False)
    address = Column(String(length=250), nullable=True)
    latitude = Column(String(length=250), nullable=False)
    longitude = Column(String(length=250), nullable=False)
    power_capacity_kw = Column(Float, nullable=False)
    available_power_capacity_kw = Column(Float, nullable=False)
    total_racks = Column(Integer, nullable=False)
    available_racks = Column(Integer, nullable=False)
    asset_id = Column(String(length=250), nullable=False)
    asset_type = Column(String(length=250), nullable=False)
    manufacturer = Column(String(length=250), nullable=False)
    model = Column(String(length=250), nullable=False)
    asset_status = Column(String(length=250), nullable=False)
    asset_location = Column(String(length=250), nullable=False)
    power_consumption_kw = Column(Float, nullable=False)
    peak_usage_kw = Column(Float, nullable=False)
    average_usage_kw = Column(Float, nullable=False)
    energy_efficiency_rating = Column(String(length=250), nullable=False)
    cooling_capacity_ton = Column(Float, nullable=False)
    current_temperature_celsius = Column(Float, nullable=False)
    cooling_unit_status = Column(String(length=250), nullable=False)
    cooling_unit_location = Column(String(length=250), nullable=False)

    # Reference to order_id in the Transaction table
    tid = Column(String(length=250), ForeignKey("transaction.tid"), nullable=True)

    # Define the relationship with Transaction based on order_id
    transaction = relationship("Transaction", back_populates="nlytes")

    @classmethod
    def from_schema(
        cls, schema: Union[schemas.NlyteCreate, schemas.NlyteUpdate], hub_id: str
    ):
        return cls(
            hub_id=hub_id,
            dc_id=schema.dc_id,
            name=schema.name,
            address=schema.location.address,
            latitude=schema.location.latitude,
            longitude=schema.location.longitude,
            power_capacity_kw=schema.power_capacity_kw,
            available_power_capacity_kw=schema.available_power_capacity_kw,
            total_racks=schema.total_racks,
            available_racks=schema.available_racks,
            asset_id=schema.asset.asset_id,
            asset_type=schema.asset.asset_type,
            manufacturer=schema.asset.manufacturer,
            model=schema.asset.model,
            asset_status=schema.asset.asset_status,
            asset_location=schema.asset.asset_location,
            power_consumption_kw=schema.energy_usage.power_consumption_kw,
            peak_usage_kw=schema.energy_usage.peak_usage_kw,
            average_usage_kw=schema.energy_usage.average_usage_kw,
            energy_efficiency_rating=schema.energy_usage.energy_efficiency_rating,
            cooling_capacity_ton=schema.cooling_unit.cooling_capacity_ton,
            current_temperature_celsius=schema.cooling_unit.current_temperature_celsius,
            cooling_unit_status=schema.cooling_unit.cooling_unit_status,
            cooling_unit_location=schema.cooling_unit.cooling_unit_location,
        )

    def to_schema(self):
        data = {
            "hub_id": self.hub_id,
            "tid": self.tid,
            "dc_id": self.dc_id,
            "name": self.name,
            "location": {
                "address": self.address,
                "latitude": self.latitude,
                "longitude": self.longitude,
            },
            "power_capacity_kw": self.power_capacity_kw,
            "available_power_capacity_kw": self.available_power_capacity_kw,
            "total_racks": self.total_racks,
            "available_racks": self.available_racks,
            "asset": {
                "asset_id": self.asset_id,
                "asset_type": self.asset_type,
                "manufacturer": self.manufacturer,
                "model": self.model,
                "asset_status": self.asset_status,
                "asset_location": self.asset_location,
            },
            "energy_usage": {
                "power_consumption_kw": self.power_consumption_kw,
                "peak_usage_kw": self.peak_usage_kw,
                "average_usage_kw": self.average_usage_kw,
                "energy_efficiency_rating": self.energy_efficiency_rating,
            },
            "cooling_unit": {
                "cooling_capacity_ton": self.cooling_capacity_ton,
                "current_temperature_celsius": self.current_temperature_celsius,
                "cooling_unit_status": self.cooling_unit_status,
                "cooling_unit_location": self.cooling_unit_location,
            },
        }
        return schemas.NlyteInDb(**data)


class Mapping(Base):
    __tablename__ = "mapping"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, default=None)
    mapping_profile = Column(String(length=250), nullable=False, unique=True)
    server_name = Column(String(length=250), nullable=False)
    rule = Column((JSONB), nullable=False)

    created_by = Column(String(length=250), nullable=True)
    modified_by = Column(String(length=250), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), server_default=func.now())

    @classmethod
    def from_schema(
        cls,
        server_name: str,
        mapping_profile: str,
        schema: Union[schemas.MappingCreate, schemas.MappingUpdate],
    ):
        return cls(
            mapping_profile=mapping_profile,
            server_name=server_name,
            rule=[rl.dict() for rl in schema.rule],
            created_by=schema.created_by,
            modified_by=schema.modified_by,
        )

    def to_schema(self):
        return schemas.MappingInDb.validate(self)


class AuthDetail(Base):
    __tablename__ = "auth_detail"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, default=None)
    server_name = Column(String(length=250), nullable=False)
    api_name = Column(String(length=250), nullable=False)
    api_url = Column(String(length=250), nullable=False)
    auth_type = Column(String(length=250), nullable=False)
    http_method = Column(String(length=250), nullable=False)
    username = Column(String(length=250), nullable=True)
    password = Column(String(length=250), nullable=True)
    bearer_token = Column(String(length=250), nullable=True)
    auth_url = Column(String(length=250), nullable=True)
    client_id = Column(String(length=250), nullable=True)
    client_secret = Column(String(length=250), nullable=True)
    scope = Column(String(length=250), nullable=True)
    grant_type = Column(String(length=250), nullable=True)

    created_by = Column(String(length=250), nullable=True)
    modified_by = Column(String(length=250), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), server_default=func.now())

    @classmethod
    def from_schema(
        cls, schema: Union[schemas.AuthDetailCreate, schemas.AuthDetailUpdate]
    ):
        return cls(
            server_name=schema.server_name,
            auth_type=schema.auth_type,
            http_method=schema.http_method,
            api_name=f"{schema.server_name.lower()}-{schema.http_method.lower()}",
            api_url=schema.api_url,
            username=schema.username,
            password=schema.password,
            bearer_token=schema.bearer_token,
            auth_url=schema.auth_url,
            client_id=schema.client_id,
            client_secret=schema.client_secret,
            scope=schema.scope,
            grant_type=schema.grant_type,
            created_by=schema.created_by,
            modified_by=schema.modified_by,
        )

    def to_schema(self):
        return schemas.AuthDetailInDb.validate(self)


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, default=None)
    tid = Column(String(length=250), nullable=False, unique=True)
    order_status = Column(String(length=250), nullable=False)

    created_by = Column(String(length=250), nullable=True)
    modified_by = Column(String(length=250), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), server_default=func.now())

    # Define the relationship with Nlyte (many-to-one from Nlyte to Transaction based on order_id)
    nlytes = relationship("Nlyte", back_populates="transaction")
    spatials = relationship("Spatial", back_populates="transaction")
    comcasts = relationship("Comcast", back_populates="transaction")

    @classmethod
    def from_schema(
        cls, schema: Union[schemas.TransactionCreate, schemas.TransactionUpdate]
    ):
        return cls(
            tid=schema.tid,
            order_status=schema.order_status,
            created_by=schema.created_by,
            modified_by=schema.modified_by,
        )

    def to_schema(self):
        return schemas.TransactionInDb.validate(self)
