from typing import List

from pydantic import BaseModel

"""
ex:
{
    "cpodIntent": {
        "cpodIntentName": "9 digit ISP name",
        "refSiteIntentName": "9 digit ISP Name",
        "refHubName": "GAL1",
        "refPpodIntentNames": "9 digit ISP Name",
    },
    "leafUplink": {
        "leafA": {
            "lag": {
                "ipv4": {"local": "", "remote": "", "subnet": ""},
                "ipv6": {"local": "", "remote": "", "subnet": ""},
            },
            "ethernetInterfaces": [
                {"localInterface": "string", "remoteInterface": "string"}
            ],
            "remoteHost": "",
        },
        "leafB": {
            "lag": {
                "ipv4": {"local": "", "remote": "", "subnet": ""},
                "ipv6": {"local": "", "remote": "", "subnet": ""},
            },
            "ethernetInterfaces": [
                [{"localInterface": "string", "remoteInterface": "string"}]
            ],
            "remoteHost": "",
        },
    },
}
"""


class CpodIntent(BaseModel):
    cpodIntentName: str
    refSiteIntentName: str
    refHubName: str
    refPpodIntentNames: str


class EthernetInterfaces(BaseModel):
    localInterface: str
    remoteInterface: str


class Ipv4Info(BaseModel):
    local: str
    remote: str
    subnet: str


class Ipv6Info(BaseModel):
    local: str
    remote: str
    subnet: str


class Lag(BaseModel):
    ipv4: Ipv4Info
    ipv6: Ipv6Info


class Leaf(BaseModel):
    lag: Lag
    ethernetInterfaces: List[EthernetInterfaces]
    remoteHost: str


class LeafUplink(BaseModel):
    leafA: Leaf
    leafB: Leaf


class CpodIntentBase(BaseModel):
    cpodIntent: CpodIntent
    leafUplink: LeafUplink
