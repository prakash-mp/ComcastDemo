from typing import List
from uuid import uuid4

from fastapi import Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from app import models, schemas, log
from app.dependencies import deps
from app.utils import write_to_comcast

router = APIRouter(tags=["Commit (Comcast Simulator)"])


@router.post("/commit")
def commit_to_comcast(
    db: Annotated[Session, Depends(deps.get_db_session)], hub_ids: List[str]
):
    tmp = {
        "tid": str(uuid4()),
        "order_type": "commit",
        "order_status": "completed",
        "created_by": "user",
        "modified_by": "user",
    }
    transaction_payload = schemas.TransactionCreate(**tmp)
    db_obj_transaction = models.Transaction.from_schema(transaction_payload)
    db.add(db_obj_transaction)

    db_objs: List[models.Comcast] = (
        db.query(models.Comcast).filter(models.Comcast.hub_id.in_(hub_ids)).all()
    )

    processed_hub_ids = []
    for db_obj in db_objs:
        if not db_obj.transaction:
            write_to_comcast.do_write(db_obj.hub_id)  # dummy function
            db_obj.tid = db_obj_transaction.tid
            processed_hub_ids.append(db_obj.hub_id)
            log.info(f"hub_id {db_obj.hub_id} committed to comcast server")

    db.commit()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "code": 201,
            "status": "OK",
            "message": f"hub ids {processed_hub_ids} found valid, initiated committing to "
            f"comcast server in background, tid {db_obj_transaction.tid} will be"
            f" updated once done",
        },
    )


@router.get("/commit/{hub_id}")
def get_commit(db: Annotated[Session, Depends(deps.get_db_session)], hub_id: str):
    db_obj: models.Comcast = (
        db.query(models.Comcast).filter(models.Comcast.hub_id == hub_id).first()
    )

    if db_obj and db_obj.transaction and db_obj.transaction.order_type == "commit":
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "status": "OK",
                "message": jsonable_encoder(db_obj.to_schema()),
            },
        )

    log.info(f"No record found for hub_id {hub_id}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "code": 404,
            "status": "Not found",
            "message": "Error",
        },
    )
