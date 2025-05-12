from typing import List

from pydantic import BaseModel

"""
ex:
{
    "daasIntent": {
        "daasIntentName": "9 digit ISP name",
        "refPpodIntentName": "9 digit ISP name",
        "refBuhmName": "Philadelphia",
        "refHubName": "GAL1",
        "refHaagIntentName": "9 digit ISP Name",
    },
    "haggConnections": {
        "ethernetInterfaces": [
            {"localInterface": "string", "remoteInterface": "string"}
        ]
    },
}
"""


class DaasIntent(BaseModel):
    daasIntentName: str
    refPpodIntentName: str
    refBuhmName: str
    refHubName: str
    refHaagIntentName: str


class EthernetInterfaces(BaseModel):
    localInterface: str
    remoteInterface: str


class HaggConnections(BaseModel):
    ethernetInterfaces: List[EthernetInterfaces]


class DaasIntentBase(BaseModel):
    daasIntent: DaasIntent
    haggConnections: HaggConnections
