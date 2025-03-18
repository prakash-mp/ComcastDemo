from typing import List
from uuid import uuid4

from fastapi import Depends, status, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from app import models, schemas, log
from app.dependencies import deps


router = APIRouter(tags=["Rogers Source Data (Spatial/Nlyte)"])


@router.get("/source-data/{api_name}")
def get_all_source_data(
    db: Annotated[Session, Depends(deps.get_db_session)],
    api_name: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
):
    db_obj_auth: models.AuthDetail = (
        db.query(models.AuthDetail)
        .filter(models.AuthDetail.api_name == api_name.lower())
        .first()
    )
    if not db_obj_auth:
        log.info(f"No record found with api {api_name}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": 404,
                "status": "Not found",
                "message": f"No record found with api {api_name}",
            },
        )

    offset = (page - 1) * page_size
    if "spatial" in db_obj_auth.api_url:
        db_objs = db.query(models.Spatial).offset(offset).limit(page_size).all()
    elif "nlyte" in db_obj_auth.api_url:
        db_objs = db.query(models.Nlyte).offset(offset).limit(page_size).all()
    else:
        db_objs = []

    for db_obj in db_objs:
        tmp = {
            "order_id": str(uuid4()),
            "hub_id": db_obj.hub_id,
            "order_status": "in-progress",
            "created_by": db_obj_auth.created_by,
            "modified_by": db_obj_auth.modified_by,
        }
        transaction_payload = schemas.TransactionCreate(**tmp)
        db_obj_transaction = models.Transaction.from_schema(transaction_payload)
        db.add(db_obj_transaction)

    db.commit()

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code": 200,
            "status": "OK",
            "message": [jsonable_encoder(db_obj.to_schema()) for db_obj in db_objs],
        },
    )
