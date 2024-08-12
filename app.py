from fastapi import FastAPI, APIRouter


app = FastAPI()

router = APIRouter()


@router.get("/ping")
def ping():
    return {"ping": "pong"}


app.include_router(router, prefix="/api/v1")
