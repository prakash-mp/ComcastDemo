from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.endpoints import (
    comcast,
    nlyte,
    custom,
    mapping,
    spatial,
    auth_detail,
    transformation,
)


app = FastAPI()
app.include_router(nlyte.router)
app.include_router(spatial.router)
app.include_router(custom.router)
app.include_router(mapping.router)
app.include_router(comcast.router)
app.include_router(auth_detail.router)
app.include_router(transformation.router)


@app.get("/", include_in_schema=False)
def redirect():
    return RedirectResponse(url="/docs")
