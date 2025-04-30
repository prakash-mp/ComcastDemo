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


router = APIRouter(tags=["Fetch Rogers Source Data (Spatial/Nlyte)"])


@router.get("/fetch/{api_name}")
def trigger_fetch_data(
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

    if (
        "spatial" not in db_obj_auth.server_name.lower()
        or "nlyte" not in db_obj_auth.server_name.lower()
    ):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": 404,
                "status": "Error",
                "message": f"Given api {api_name} does not belong to any of "
                f"the source server among spatial/nlyte",
            },
        )

    tmp = {
        "tid": str(uuid4()),
        "order_type": "fetch",
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
            "message": f"records are being fetched in background, tid "
            f"{db_obj_transaction.tid} will be updated once done",
        },
    )
