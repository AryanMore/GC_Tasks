from fastapi import FastAPI
from Router_Functions.router import router
from qdrant_connect import create_collection

app = FastAPI(title="Document Vector CRUD API")

create_collection()

app.include_router(router)
