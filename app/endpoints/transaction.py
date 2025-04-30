from typing import List

from fastapi import Depends, status, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from app import models, schemas, log
from app.dependencies import deps


router = APIRouter(tags=["Transaction"])


@router.get("/transactions")
def get_all_transactions(
    db: Annotated[Session, Depends(deps.get_db_session)],
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
):
    offset = (page - 1) * page_size
    db_objs: List[models.Transaction] = (
        db.query(models.Transaction).offset(offset).limit(page_size).all()
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code": 200,
            "status": "OK",
            "message": [jsonable_encoder(db_obj.to_schema()) for db_obj in db_objs],
        },
    )
