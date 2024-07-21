from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def default_route():
    return {"message": "Hitting the default Route"}