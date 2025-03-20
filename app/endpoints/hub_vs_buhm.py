from typing import List

from fastapi import Depends, status, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from app import models, schemas, log
from app.dependencies import deps

router = APIRouter(tags=["Hub Vs Buhm"])


@router.post("/hub_vs_buhm")
def create_hub_vs_buhm(
    db: Annotated[Session, Depends(deps.get_db_session)],
    data_in: schemas.HubVsBuhmCreate,
):
    db_obj = (
        db.query(models.HubVsBuhm)
        .filter(models.HubVsBuhm.hub_id == data_in.hub_id)
        .first()
    )
    if db_obj:
        log.info(f"Record already exists for hub_id {data_in.hub_id}")
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "code": 409,
                "status": "Conflict",
                "message": f"Record already exists for hub_id {data_in.hub_id}",
            },
        )

    db_obj = models.HubVsBuhm.from_schema(data_in)
    db.add(db_obj)
    db.commit()

    log.info(
        f"hub to buhm mapping created for hub id {data_in.hub_id} "
        f"and buhm id {data_in.BuhmId}"
    )

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "code": 201,
            "status": "OK",
            "message": jsonable_encoder(db_obj.to_schema()),
        },
    )


@router.get("/hub_vs_buhm/{hub_id}")
def get_hub_vs_buhm(
    db: Annotated[Session, Depends(deps.get_db_session)],
    hub_id: str,
):
    db_obj = (
        db.query(models.HubVsBuhm).filter(models.HubVsBuhm.hub_id == hub_id).first()
    )
    if not db_obj:
        log.info(f"No record found for hub id {hub_id}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": 404,
                "status": "Not found",
                "message": f"No record found for hub id {hub_id}",
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


@router.get("/hub_vs_buhm")
def get_all_hub_vs_buhm(
    db: Annotated[Session, Depends(deps.get_db_session)],
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
):
    offset = (page - 1) * page_size

    db_objs: List[models.HubVsBuhm] = (
        db.query(models.HubVsBuhm).offset(offset).limit(page_size).all()
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code": 200,
            "status": "OK",
            "message": [jsonable_encoder(db_obj.to_schema()) for db_obj in db_objs],
        },
    )


@router.put("/hub_vs_buhm/{hub_id}")
def update_hub_vs_buhm(
    db: Annotated[Session, Depends(deps.get_db_session)],
    hub_id: str,
    data_in: schemas.HubVsBuhmUpdate,
):
    db_obj: models.HubVsBuhm = (
        db.query(models.HubVsBuhm).filter(models.HubVsBuhm.hub_id == hub_id).first()
    )
    if not db_obj:
        log.info(f"No record found for hub id {hub_id}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": 404,
                "status": "Not found",
                "message": f"No record found for hub id {hub_id}",
            },
        )

    db_obj.BuhmId = data_in.BuhmId
    db.commit()
    db.refresh(db_obj)

    log.info(f"Record updated for hub_id {hub_id}")

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code": 200,
            "status": "OK",
            "message": jsonable_encoder(db_obj.to_schema()),
        },
    )


@router.delete("/hub_vs_buhm/{hub_id}")
def delete_hub_vs_buhm(
    db: Annotated[Session, Depends(deps.get_db_session)],
    hub_id: str,
):
    db_obj = (
        db.query(models.HubVsBuhm).filter(models.HubVsBuhm.hub_id == hub_id).first()
    )
    if not db_obj:
        log.info(f"No record found for hub id {hub_id}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": 404,
                "status": "Not found",
                "message": f"No record found for hub id {hub_id}",
            },
        )

    db.delete(db_obj)
    db.commit()
    log.info(f"Record deleted for hub_id {hub_id}")
    return status.HTTP_204_NO_CONTENT
