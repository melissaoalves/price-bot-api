from fastapi import FastAPI
from app.routes import router

app = FastAPI(
    title="Price Bot API",
    description="Uma API para automatizar a raspagem de preços de produtos e consultar seu histórico.",
    version="1.0.0"
)

@app.get("/", tags=["Root"])
def root():
    return {"message": "Bem-vindo à Price Bot API!"}

app.include_router(router, prefix="/api", tags=["Products"])

