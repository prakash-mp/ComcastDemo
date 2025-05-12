from pydantic import BaseModel

"""
ex:
{
        "hubName": "GAL1",
        "hubType": "Primary",
        "parentHubName": "GAL2",
        "refBuhmName": "Philadelphia",
        "postalAddress": {
            "addr1": "375 Rockbridge Rd NW",
            "addr2": "Unit 2",
            "administrativeArea": "PA",
            "country": "US",
            "postalCode": ""
        },
        "timezone": "GMT"
    }
"""


class PostalAddress(BaseModel):
    addr1: str
    addr2: str
    administrativeArea: str
    country: str
    postalCode: str


class HubBase(BaseModel):
    hubName: str
    hubType: str
    parentHubName: str
    refBuhmName: str
    postalAddress: PostalAddress
    timezone: str
