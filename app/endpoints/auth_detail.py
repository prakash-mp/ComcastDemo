from typing import List

from fastapi import Depends, status, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from app import models, schemas, log
from app.dependencies import deps


router = APIRouter(tags=["Server Onboard"])


@router.post("/auth_detail")
def create_auth(
    db: Annotated[Session, Depends(deps.get_db_session)],
    data_in: schemas.AuthDetailCreate,
):
    api_name = f"{data_in.server_name.lower()}-{data_in.http_method.lower()}"
    db_obj = (
        db.query(models.AuthDetail)
        .filter(models.AuthDetail.api_name == api_name.lower())
        .first()
    )
    if db_obj:
        log.info(f"Record already exists for server_name-http_method {api_name}")
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "code": 409,
                "status": "Conflict",
                "message": "Error",
            },
        )

    db_obj = models.AuthDetail.from_schema(schema=data_in)

    db.add(db_obj)
    db.commit()

    log.info(f"Auth record created as auth_id {db_obj.id}")

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "code": 201,
            "status": "OK",
            "message": jsonable_encoder(db_obj.to_schema()),
        },
    )


@router.get("/auth_detail/{api_name}")
def get_auth(db: Annotated[Session, Depends(deps.get_db_session)], api_name: str):
    db_obj = (
        db.query(models.AuthDetail)
        .filter(models.AuthDetail.api_name == api_name.lower())
        .first()
    )
    if not db_obj:
        log.info(f"No record found for api_name {api_name}")
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


@router.get("/auth_detail")
def get_all_auth(
    db: Annotated[Session, Depends(deps.get_db_session)],
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
):
    offset = (page - 1) * page_size
    db_objs: List[models.AuthDetail] = (
        db.query(models.AuthDetail).offset(offset).limit(page_size).all()
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code": 200,
            "status": "OK",
            "message": [jsonable_encoder(db_obj.to_schema()) for db_obj in db_objs],
        },
    )


@router.put("/auth_detail/{api_name}")
def update_auth(
    db: Annotated[Session, Depends(deps.get_db_session)],
    data_in: schemas.AuthDetailUpdate,
    api_name: str,
):
    db_obj: models.AuthDetail = (
        db.query(models.AuthDetail)
        .filter(models.AuthDetail.api_name == api_name.lower())
        .first()
    )
    if not db_obj:
        log.info(f"No record found for api {api_name}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": 404,
                "status": "Not found",
                "message": "Error",
            },
        )

    obj_data = jsonable_encoder(db_obj)
    data_in = data_in.dict()
    for attribute in obj_data:
        if attribute in data_in:
            setattr(db_obj, attribute, data_in[attribute])

    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    log.info(f"Record updated for api {api_name}")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code": 200,
            "status": "OK",
            "message": jsonable_encoder(db_obj.to_schema()),
        },
    )


@router.delete("/auth_detail/{api_name}")
def delete_auth(
    db: Annotated[Session, Depends(deps.get_db_session)],
    api_name: str,
):
    db_obj = (
        db.query(models.AuthDetail)
        .filter(models.AuthDetail.api_name == api_name.lower())
        .first()
    )
    if not db_obj:
        log.info(f"No record found for api {api_name}")
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
    log.info(f"Record deleted for api {api_name}")
    return status.HTTP_204_NO_CONTENT
