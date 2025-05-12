from typing import List

from pydantic import BaseModel

"""
ex:
{
    "haggintent": {
        "haggIntentName": "9 digit ISP name",
        "refPpodIntentName": "9 digit ISP Name",
        "refSiteIntentName": "9 digit ISP Name",
        "refBuhmName": "Philadelphia",
        "refHubName": "GAL1",
    },
    "maggConnections": {
        "ethernetInterfaces": [
            {"localInterface": "string", "remoteInterface": "string"}
        ]
    },
}
"""


class HaggIntent(BaseModel):
    haggIntentName: str
    refPpodIntentName: str
    refSiteIntentName: str
    refBuhmName: str
    refHubName: str


class EthernetInterfaces(BaseModel):
    localInterface: str
    remoteInterface: str


class MaggConnections(BaseModel):
    ethernetInterfaces: List[EthernetInterfaces]


class HaggIntentBase(BaseModel):
    haggintent: HaggIntent
    maggConnections: MaggConnections
