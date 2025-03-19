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
from app.utils import mapper


router = APIRouter(tags=["Stage"])


@router.get("/stage/{mapping_profile}/{tid}")
def get_staged_data_mapping_profile_and_tid(
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


@router.get("/stage/{mapping_profile}")
def get_staged_data_for_mapping_profile(
    db: Annotated[Session, Depends(deps.get_db_session)],
    mapping_profile: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1),
):
    offset = (page - 1) * page_size
    if mapping_profile.lower() == "custom":
        db_objs = (
            db.query(models.Comcast)
            .filter(models.Comcast.transaction.has(order_type="fetch"))
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
                .filter(models.Spatial.transaction.has(order_type="fetch"))
                .offset(offset)
                .limit(page_size)
                .all()
            )
        elif "nlyte" in db_obj_mapping.server_name.lower():
            db_objs = (
                db.query(models.Nlyte)
                .filter(models.Nlyte.transaction.has(order_type="fetch"))
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


@router.post("/stage/transform/{mapping_profile}")
def transform(
    db: Annotated[Session, Depends(deps.get_db_session)],
    hub_ids: List[str],
    mapping_profile: str,
):
    tmp = {
        "tid": str(uuid4()),
        "order_type": "stage",
        "order_status": "completed",
        "created_by": "user",
        "modified_by": "user",
    }
    transaction_payload = schemas.TransactionCreate(**tmp)
    db_obj_transaction = models.Transaction.from_schema(transaction_payload)
    db.add(db_obj_transaction)

    db_obj_mapping = (
        db.query(models.Mapping)
        .filter(models.Mapping.mapping_profile == mapping_profile)
        .first()
    )
    if not db_obj_mapping and mapping_profile.lower() != "custom":
        log.info(f"No mapping record found for given mapping profile {mapping_profile}")
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "code": 404,
                "status": "Not found",
                "message": "Mapping profile does not exist",
            },
        )

    if db_obj_mapping and "spatial" in db_obj_mapping.server_name.lower():
        db_objs = (
            db.query(models.Spatial).filter(models.Spatial.hub_id.in_(hub_ids)).all()
        )

    elif db_obj_mapping and "nlyte" in db_obj_mapping.server_name.lower():
        db_objs = db.query(models.Nlyte).filter(models.Nlyte.hub_id.in_(hub_ids)).all()

    else:
        db_objs = (
            db.query(models.Comcast).filter(models.Comcast.hub_id.in_(hub_ids)).all()
        )

    processed_hub_ids = []
    for db_obj in db_objs:
        if (
            db_obj.transaction.order_type == "fetch"
            and db_obj_transaction.order_status == "completed"
        ):
            if mapping_profile.lower() != "custom":
                source_data = db_obj.to_schema()
                try:
                    mapped_data: schemas.ComcastCreate = mapper.do_mapping(
                        data_in=source_data, db_obj_mapping=db_obj_mapping
                    )
                except Exception as exc:
                    log.info(f"mapping error for hub id: {db_obj.hub_id}: {exc}")
                    continue

                db_obj_mapped: models.Comcast = models.Comcast.from_schema(mapped_data)
                db.add(db_obj_mapped)

            db_obj.tid = db_obj_transaction.tid
            processed_hub_ids.append(db_obj.hub_id)

            log.info(
                f"Transformation done from source to comcast for hub_id {db_obj.hub_id}"
            )

    db.commit()

    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content={
            "code": 201,
            "status": "OK",
            "message": f"hub ids {processed_hub_ids} found valid & transformation "
            f"initiated in background, tid {db_obj_transaction.tid} will be updated once done",
        },
    )
