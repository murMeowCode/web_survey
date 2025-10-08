"""main для сервиса"""
from fastapi import FastAPI,APIRouter
from main_auth.api.auth import router as auth_router
from main_auth.api.users import router as user_router
from main_auth.api.oauth import router as oauth_router
from main_auth.core.nats_utils import on_shutdown

router = APIRouter()
router.include_router(router=auth_router)
router.include_router(router=user_router)
router.include_router(router=oauth_router)

app = FastAPI()
app.include_router(router)
app.add_event_handler("shutdown", on_shutdown)
