"""main для сервиса"""
from fastapi import FastAPI,APIRouter
from main_auth.api.auth import router as auth_router

router = APIRouter()
router.include_router(router=auth_router)

app = FastAPI()
app.include_router(router)
