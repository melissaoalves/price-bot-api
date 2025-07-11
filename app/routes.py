from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def root():
    return {"message": "API do Bot de Preços está no ar!"}
