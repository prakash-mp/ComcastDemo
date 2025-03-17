from fastapi import Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from app import models, schemas, log
from app.dependencies import deps

router = APIRouter(tags=["Comcast Simulator"])


@router.post("/comcast/hubs")
def create_comcast(
    db: Annotated[Session, Depends(deps.get_db_session)], data_in: schemas.ComcastCreate
):
    db_obj = (
        db.query(models.Comcast).filter(models.Comcast.hub_id == data_in.hub_id).first()
    )
    if not db_obj:
        log.info(f"No record found for hub_id {data_in.hub_id}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": 404,
                "status": "Not found",
                "message": "Error",
            },
        )
    log.info(f"Record created for hub_id {data_in.hub_id}")
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content={"Result": "Created"}
    )


@router.get("/comcast/hubs/{hub_id}")
def get_comcast(db: Annotated[Session, Depends(deps.get_db_session)], hub_id: str):
    db_obj = db.query(models.Comcast).filter(models.Comcast.hub_id == hub_id).first()
    if not db_obj:
        log.info(f"No record found for hub_id {hub_id}")
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
