from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Price Bot API")

app.include_router(router)
