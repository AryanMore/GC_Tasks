from fastapi import FastAPI
from Endpoints.routes import router

app = FastAPI()
app.include_router(router)
