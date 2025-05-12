from pydantic import BaseModel


"""
ex:
{
        "nodesegIntent": {
            "nodesegIntentName": "10 digit OSP name",
            "refRpdIntentName": "10 digit OSP name"
        },
        "usePort": 0
    }
"""


class NodeSegIntent(BaseModel):
    nodesegIntentName: str
    refRpdIntentName: str


class NodeSegIntentBase(BaseModel):
    nodesegIntent: NodeSegIntent
    usePort: int
