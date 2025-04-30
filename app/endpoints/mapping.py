from typing import List

from fastapi import Depends, status, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from app import models, schemas, log
from app.dependencies import deps

router = APIRouter(tags=["Mapping"])


@router.post("/mappings/{mapping_profile}/{server_name}")
def create_mapping(
    db: Annotated[Session, Depends(deps.get_db_session)],
    mapping_profile: str,
    server_name: str,
    data_in: schemas.MappingCreate,
):
    db_obj = (
        db.query(models.AuthDetail)
        .filter(models.AuthDetail.server_name == server_name)
        .first()
    )
    if not db_obj:
        log.info(f"No Record found for server name {server_name}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": 404,
                "status": "Not found",
                "message": "Server name not found",
            },
        )

    db_obj = (
        db.query(models.Mapping)
        .filter(models.Mapping.mapping_profile == mapping_profile)
        .first()
    )
    if db_obj:
        log.info(f"Record already exists for mapping profile {mapping_profile}")
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"code": 409, "status": "Conflict", "message": "Error"},
        )

    db_obj = models.Mapping.from_schema(
        server_name=server_name, mapping_profile=mapping_profile, schema=data_in
    )

    db.add(db_obj)
    db.commit()
    log.info(f"Record created for mapping profile {mapping_profile}")
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "code": 201,
            "status": "OK",
            "message": jsonable_encoder(db_obj.to_schema()),
        },
    )


@router.get("/mappings/{mapping_profile}")
def get_mapping(
    db: Annotated[Session, Depends(deps.get_db_session)],
    mapping_profile: str,
):
    db_obj = (
        db.query(models.Mapping)
        .filter(models.Mapping.mapping_profile == mapping_profile)
        .first()
    )
    if not db_obj:
        log.info(f"No Record found for mapping profile {mapping_profile}")
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


@router.get("/mappings")
def get_all_mapping(
    db: Annotated[Session, Depends(deps.get_db_session)],
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
):
    offset = (page - 1) * page_size
    db_objs: List[models.Mapping] = (
        db.query(models.Mapping).offset(offset).limit(page_size).all()
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code": 200,
            "status": "OK",
            "message": [jsonable_encoder(db_obj.to_schema()) for db_obj in db_objs],
        },
    )


@router.put("/mappings/{mapping_profile}")
def update_mapping(
    db: Annotated[Session, Depends(deps.get_db_session)],
    mapping_profile: str,
    data_in: schemas.MappingUpdate,
):
    db_obj: models.Mapping = (
        db.query(models.Mapping)
        .filter(models.Mapping.mapping_profile == mapping_profile)
        .first()
    )
    if not db_obj:
        log.info(f"No Record found for mapping profile {mapping_profile}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": 404,
                "status": "Not found",
                "message": "Error",
            },
        )

    obj_data = jsonable_encoder(db_obj)
    data_in = jsonable_encoder(data_in)
    for attribute in obj_data:
        if attribute in data_in:
            setattr(db_obj, attribute, data_in[attribute])

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    log.info(f"Record updated for mapping profile {mapping_profile}")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code": 200,
            "status": "OK",
            "message": jsonable_encoder(db_obj.to_schema()),
        },
    )


@router.delete("/mappings/{mapping_profile}")
def delete_mapping(
    db: Annotated[Session, Depends(deps.get_db_session)],
    mapping_profile: str,
):
    db_obj = (
        db.query(models.Mapping)
        .filter(models.Mapping.mapping_profile == mapping_profile)
        .first()
    )
    if not db_obj:
        log.info(f"No Record found for mapping profile {mapping_profile}")
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
    log.info(f"Record deleted for mapping profile {mapping_profile}")
    return status.HTTP_204_NO_CONTENT
