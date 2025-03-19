from fastapi import Depends, status, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from pydantic import ValidationError
from typing_extensions import Annotated

from app import models, schemas, log
from app.dependencies import deps
from app.utils import mapper


router = APIRouter(tags=["Stage"])


@router.get("/stage/{mapping_profile}/{tid}")
def get_staged_data(
    db: Annotated[Session, Depends(deps.get_db_session)],
    mapping_profile: str,
    tid: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
):
    offset = (page - 1) * page_size
    if mapping_profile.lower() == "custom":
        db_objs = (
            db.query(models.Comcast)
            .filter(models.Comcast.tid == tid)
            .offset(offset)
            .limit(page_size)
            .all()
        )
    else:
        db_obj_mapping: models.Mapping = (
            db.query(models.Mapping)
            .filter(models.Mapping.mapping_profile == mapping_profile)
            .first()
        )
        if not db_obj_mapping:
            log.info(f"Profile {mapping_profile} does not exist")
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "code": 404,
                    "status": "Not found",
                    "message": f"Profile {mapping_profile} does not exist",
                },
            )
        if "spatial" in db_obj_mapping.server_name.lower():
            db_objs = (
                db.query(models.Spatial)
                .filter(models.Spatial.tid == tid)
                .offset(offset)
                .limit(page_size)
                .all()
            )
        elif "nlyte" in db_obj_mapping.server_name.lower():
            db_objs = (
                db.query(models.Nlyte)
                .filter(models.Nlyte.tid == tid)
                .offset(offset)
                .limit(page_size)
                .all()
            )
        else:
            db_objs = []

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code": 200,
            "status": "OK",
            "message": [jsonable_encoder(db_obj.to_schema()) for db_obj in db_objs],
        },
    )


@router.post("/transform/nlyte/{mapping_profile}")
def transform_nlyte(
    db: Annotated[Session, Depends(deps.get_db_session)],
    data_in: schemas.NlyteInDb,
    mapping_profile: str,
):
    db_obj_mapping = (
        db.query(models.Mapping)
        .filter(models.Mapping.mapping_profile == mapping_profile)
        .first()
    )
    if not db_obj_mapping:
        log.info(f"No mapping record found for given mapping profile {mapping_profile}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": 404,
                "status": "Not found",
                "message": "Mapping profile does not exist",
            },
        )

    db_obj = (
        db.query(models.Nlyte).filter(models.Nlyte.hub_id == data_in.hub_id).first()
    )
    if not db_obj:
        log.info(f"No record found for given hub_id {data_in.hub_id}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": 404,
                "status": "Not found",
                "message": "Error",
            },
        )

    try:
        mapped_data: schemas.ComcastCreate = mapper.do_mapping(
            data_in=data_in, db_obj_mapping=db_obj_mapping
        )
    except Exception as exc:
        raise ValidationError(exc)

    db_obj: models.Comcast = models.Comcast.from_schema(mapped_data)
    db.add(db_obj)
    db.commit()
    log.info(f"Transformation done from nlyte to Comcast for hub_id {data_in.hub_id}")
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "code": 201,
            "status": "OK",
            "message": jsonable_encoder(db_obj.to_schema()),
        },
    )


@router.post("/transform/spatial/{mapping_profile}")
def transform_spatial(
    db: Annotated[Session, Depends(deps.get_db_session)],
    data_in: schemas.SpatialInDb,
    mapping_profile: str,
):
    db_obj_mapping = (
        db.query(models.Mapping)
        .filter(models.Mapping.mapping_profile == mapping_profile)
        .first()
    )
    if not db_obj_mapping:
        log.info(f"No mapping record found for given mapping profile {mapping_profile}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": 404,
                "status": "Not found",
                "message": "Mapping profile does not exist",
            },
        )

    db_obj = (
        db.query(models.Nlyte).filter(models.Nlyte.hub_id == data_in.hub_id).first()
    )
    if not db_obj:
        log.info(f"No record found for given hub_id {data_in.hub_id}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": 404,
                "status": "Not found",
                "message": "Error",
            },
        )

    try:
        mapped_data: schemas.ComcastCreate = mapper.do_mapping(
            data_in=data_in, db_obj_mapping=db_obj_mapping
        )
    except Exception as exc:
        raise ValidationError(exc)

    db_obj: models.Comcast = models.Comcast.from_schema(mapped_data)
    db.add(db_obj)
    db.commit()
    log.info(f"Transformation done from spatial to Comcast for hub_id {data_in.hub_id}")
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "code": 201,
            "status": "OK",
            "message": jsonable_encoder(db_obj.to_schema()),
        },
    )


@router.post("/transform/custom/{mapping_profile}")
def transform_custom(
    db: Annotated[Session, Depends(deps.get_db_session)],
    data_in: schemas.ComcastInDb,
    mapping_profile: str,
):
    db_obj_mapping = (
        db.query(models.Mapping)
        .filter(models.Mapping.mapping_profile == mapping_profile)
        .first()
    )
    if not db_obj_mapping:
        log.info(f"No mapping record found for given mapping profile {mapping_profile}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": 404,
                "status": "Not found",
                "message": "Mapping profile does not exist",
            },
        )

    db_obj = (
        db.query(models.Nlyte).filter(models.Nlyte.hub_id == data_in.hub_id).first()
    )
    if not db_obj:
        log.info(f"No record found for given hub_id {data_in.hub_id}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": 404,
                "status": "Not found",
                "message": "Error",
            },
        )
    log.info(f"Transformation done from custom to Comcast for hub_id {data_in.hub_id}")
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "code": 201,
            "status": "OK",
            "message": jsonable_encoder(db_obj.to_schema()),
        },
    )
