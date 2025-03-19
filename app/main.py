from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

from app.endpoints import (
    commit,
    nlyte,
    custom,
    mapping,
    spatial,
    auth_detail,
    stage,
    transaction,
    fetch,
)

app = FastAPI(title="ComcastDemo")
app.include_router(nlyte.router)
app.include_router(spatial.router)
app.include_router(auth_detail.router)
app.include_router(mapping.router)
app.include_router(fetch.router)
app.include_router(custom.router)
app.include_router(stage.router)
app.include_router(commit.router)
app.include_router(transaction.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
def redirect():
    return RedirectResponse(url="/docs")
