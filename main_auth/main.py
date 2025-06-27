"""main для сервиса"""
from fastapi import FastAPI,APIRouter
from main_auth.api.auth import router as auth_router
from main_auth.api.users import router as user_router

router = APIRouter()
router.include_router(router=auth_router)
router.include_router(router=user_router)

app = FastAPI()
app.include_router(router)
