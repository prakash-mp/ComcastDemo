from uuid import uuid4
from typing import List

from fastapi import Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from app import models, schemas, log
from app.dependencies import deps


router = APIRouter(tags=["Spatial Simulator"])


@router.post("/spatial/hubs")
def create_spatial_hub(
    db: Annotated[Session, Depends(deps.get_db_session)], data_in: schemas.SpatialCreate
):
    hub_id = str(uuid4())
    db_obj = models.Spatial.from_schema(schema=data_in, hub_id=hub_id)

    db.add(db_obj)
    db.commit()
    log.info(f"Record created with hub_id {db_obj.hub_id}")
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "code": 201,
            "status": "OK",
            "message": jsonable_encoder(db_obj.to_schema()),
        },
    )


@router.get("/spatial/hubs/{hub_id}")
def get_spatial_hub(db: Annotated[Session, Depends(deps.get_db_session)], hub_id: str):
    db_obj = db.query(models.Spatial).filter(models.Spatial.hub_id == hub_id).first()
    if not db_obj:
        log.info(f"No record found with hub_id {hub_id}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": 404,
                "status": "Not found",
                "message": "Error",
            },
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code": 200,
            "status": "OK",
            "message": jsonable_encoder(db_obj.to_schema()),
        },
    )


@router.get("/spatial/hubs")
def get_all_spatial_hub(db: Annotated[Session, Depends(deps.get_db_session)]):
    db_objs: List[models.Spatial] = db.query(models.Spatial).all()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code": 200,
            "status": "OK",
            "message": [jsonable_encoder(db_obj.to_schema()) for db_obj in db_objs],
        },
    )


@router.patch("/spatial/hubs/{hub_id}")
def update_spatial_hub(
    db: Annotated[Session, Depends(deps.get_db_session)],
    hub_id: str,
    data_in: schemas.SpatialUpdate,
):
    db_obj = db.query(models.Spatial).filter(models.Spatial.hub_id == hub_id).first()
    if not db_obj:
        log.info(f"No record found with hub_id {hub_id}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": 404,
                "status": "Not found",
                "message": "Error",
            },
        )

    db_obj.name = data_in.name
    db_obj.region = data_in.region
    db_obj.address = data_in.location.address
    db_obj.latitude = data_in.location.latitude
    db_obj.longitude = data_in.location.longitude
    db_obj.power_capacity_kw = data_in.infrastructure.power_capacity_kw
    db_obj.cooling_capacity_ton = data_in.infrastructure.cooling_capacity_ton
    db_obj.infrastructure_type = data_in.infrastructure.infrastructure_type
    db_obj.infrastructure_status = data_in.infrastructure.infrastructure_status
    db_obj.infrastructure_capacity = data_in.infrastructure.infrastructure_capacity
    db_obj.propagation_distance_km = data_in.signal_propagation.propagation_distance_km
    db_obj.terrain_type = data_in.signal_propagation.terrain_type
    db_obj.signal_loss_db = data_in.signal_propagation.signal_loss_db
    db_obj.interference_level_db = data_in.signal_propagation.interference_level_db
    db_obj.coverage_area_km2 = data_in.network_coverage.coverage_area_km2
    db_obj.signal_strength_dbm = data_in.network_coverage.signal_strength_dbm
    db_obj.network_type = data_in.network_coverage.network_type

    db.commit()
    db.refresh(db_obj)

    log.info(f"Updated the spatial record for hub id {hub_id}")

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code": 200,
            "status": "OK",
            "message": jsonable_encoder(db_obj.to_schema()),
        },
    )


@router.delete("/spatial/hubs/{hub_id}")
def delete_spatial_hub(
    db: Annotated[Session, Depends(deps.get_db_session)], hub_id: str
):
    db_obj = db.query(models.Spatial).filter(models.Spatial.hub_id == hub_id).first()
    if not db_obj:
        log.info(f"No record found with hub_id {hub_id}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": 404,
                "status": "Not found",
                "message": "Error",
            },
        )

    db.delete(db_obj)
    db.commit()
    log.info(f"Record deleted for hub_id {hub_id}")
    return status.HTTP_204_NO_CONTENT
