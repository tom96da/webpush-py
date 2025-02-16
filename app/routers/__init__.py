from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.get("/health")
def read_health():
    return {"status": "ok"}
