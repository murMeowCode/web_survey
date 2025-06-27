"""main для сервиса"""
from fastapi import FastAPI,APIRouter
from main_auth.api.user import router as api_router

router = APIRouter()
router.include_router(router=api_router)

app = FastAPI()
