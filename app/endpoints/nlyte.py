from typing import List
from uuid import uuid4

from fastapi import Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from app import models, schemas, log
from app.dependencies import deps


router = APIRouter(tags=["NLType Simulator"])


@router.post("/nlyte/hubs")
def create_nlyte_hub(
    db: Annotated[Session, Depends(deps.get_db_session)], data_in: schemas.NlyteCreate
):
    hub_id = str(uuid4())
    db_obj = models.Nlyte.from_schema(schema=data_in, hub_id=hub_id)

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


@router.get("/nlyte/hubs/{hub_id}")
def get_nlyte_hub(db: Annotated[Session, Depends(deps.get_db_session)], hub_id: str):
    db_obj = db.query(models.Nlyte).filter(models.Nlyte.hub_id == hub_id).first()
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


@router.get("/nlyte/hubs")
def get_all_nlyte_hub(db: Annotated[Session, Depends(deps.get_db_session)]):
    db_objs: List[models.Nlyte] = db.query(models.Nlyte).all()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code": 200,
            "status": "OK",
            "message": [jsonable_encoder(db_obj.to_schema()) for db_obj in db_objs],
        },
    )


@router.put("/nlyte/hubs/{hub_id}")
def update_nlyte_hub(
    db: Annotated[Session, Depends(deps.get_db_session)],
    hub_id: str,
    data_in: schemas.NlyteUpdate,
):
    db_obj = db.query(models.Nlyte).filter(models.Nlyte.hub_id == hub_id).first()
    if not db_obj:
        log.info(f"No record found with hub_id {hub_id}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": 404,
                "status": "Not found",
                "message": f"No record found with hub_id {hub_id}",
            },
        )

    db_obj.dc_id = data_in.dc_id
    db_obj.name = data_in.name
    db_obj.address = data_in.location.address
    db_obj.latitude = data_in.location.latitude
    db_obj.longitude = data_in.location.longitude
    db_obj.power_capacity_kw = data_in.power_capacity_kw
    db_obj.available_power_capacity_kw = data_in.available_power_capacity_kw
    db_obj.total_racks = data_in.total_racks
    db_obj.available_racks = data_in.available_racks
    db_obj.asset_id = data_in.asset.asset_id
    db_obj.asset_type = data_in.asset.asset_type
    db_obj.manufacturer = data_in.asset.manufacturer
    db_obj.model = data_in.asset.model
    db_obj.asset_status = data_in.asset.asset_status
    db_obj.asset_location = data_in.asset.asset_location
    db_obj.power_consumption_kw = data_in.energy_usage.power_consumption_kw
    db_obj.peak_usage_kw = data_in.energy_usage.peak_usage_kw
    db_obj.average_usage_kw = data_in.energy_usage.average_usage_kw
    db_obj.energy_efficiency_rating = data_in.energy_usage.energy_efficiency_rating
    db_obj.cooling_capacity_ton = data_in.cooling_unit.cooling_capacity_ton
    db_obj.current_temperature_celsius = (
        data_in.cooling_unit.current_temperature_celsius
    )
    db_obj.cooling_unit_status = data_in.cooling_unit.cooling_unit_status
    db_obj.cooling_unit_location = data_in.cooling_unit.cooling_unit_location

    db.commit()

    log.info(f"nlyte data updated for the hub id {hub_id}")

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code": 200,
            "status": "OK",
            "message": jsonable_encoder(db_obj.to_schema()),
        },
    )


@router.delete("/nlyte/hubs/{hub_id}")
def delete_nlyte_hub(db: Annotated[Session, Depends(deps.get_db_session)], hub_id: str):
    db_obj = db.query(models.Nlyte).filter(models.Nlyte.hub_id == hub_id).first()
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
