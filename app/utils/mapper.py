from typing import Union

import faker
from fastapi.encoders import jsonable_encoder

from app import schemas, models, log


dummy = faker.Faker()


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
            "hubName": data_in.name,
            "hubType": "primary",
            "primaryHubId": "5ede4d9cf41a0058f1949bbe",
            "addr1": data_in.location.address,
            "addr2": data_in.location.address,
            "city": dummy.city(),
            "BuhmId": "",
            "countryCode": dummy.country_code(),
            "locality": "locality",
            "serviceStatus": "I",
            "state": dummy.state(),
            "zipCode": dummy.zipcode(),
            "timezone": "EST",
            "location": {
                "type": "Point",
                "coordinates": [str(dummy.longitude()), str(dummy.latitude())],
            },
        },
        "createdBy": dummy.name(),
        "modifiedBy": dummy.name(),
    }
    return schemas.ComcastCreate(**dummy_destination_data)
