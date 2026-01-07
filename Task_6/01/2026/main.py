from fastapi import FastAPI
from routes import router as product_router

app = FastAPI(title="Product CRUD API")

app.include_router(product_router)
