from typing import Union

from fastapi.encoders import jsonable_encoder

from app import schemas, models, log


def do_mapping(
    data_in: Union[schemas.SpatialInDb, schemas.NlyteInDb],
    db_obj_mapping: models.Mapping,
) -> schemas.ComcastCreate:
    # destination_data = dict()
    # for rl in db_obj_mapping.rule:
    #     source_keys = rl.get("source").split(".")
    #     destination_keys = rl.get("destination").split(".")
    #     optional = rl.get("optional")
    #
    #     value = jsonable_encoder(data_in)
    #     for k in source_keys:
    #         if k not in value:
    #             log.info(
    #                 f"key {k} from mapping profile {db_obj_mapping.mapping_profile} "
    #                 f"is missing in source data having hub_id {data_in.hub_id} "
    #             )
    #             raise Exception(f"key {k} is missing in source data")
    #         value = value[k]
    #
    #     temp = destination_data
    #     for i, key in enumerate(destination_keys):
    #         if i == len(destination_keys) - 1:
    #             temp[key] = value
    #         else:
    #             temp = temp.setdefault(key, {})

    dummy_destination_data = {
        "partner": ["comcast", "rogers"],
        "hub_id": data_in.hub_id,
        "hub": {
            "hubCode": "GAL1",
            "hubName": "Aurora.CO",
            "hubType": "primary",
            "primaryHubId": "5ede4d9cf41a0058f1949bbe",
            "addr1": "375 Rockbridge Rd NW",
            "addr2": "Unit 2",
            "city": "LILBURN",
            "BuhmId": "5ede4d9cf41a0058f1949bbe",
            "countryCode": "CAN",
            "locality": "locality",
            "serviceStatus": "I",
            "state": "GA",
            "zipCode": "30047",
            "timezone": "EST",
            "location": {"type": "Point", "coordinates": [-84.16322687, 33.88408157]},
        },
        "createdBy": "user",
        "modifiedBy": "user",
    }
    return schemas.ComcastCreate(**dummy_destination_data)
