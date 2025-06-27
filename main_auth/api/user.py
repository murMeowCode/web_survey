"""routers for users ops"""
from fastapi import APIRouter,HTTPException

from main_auth.core.auth import auth_backend, fastapi_users
from main_auth.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth']
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth']
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users']
)

@router.delete('/users/{id}', tags=['users'], deprecated=True)
def delete_user(id: int):  #pylint: disable=W0622
    """Не используйте удаление, деактивируйте пользователей."""
    raise HTTPException(
        status_code=405,
        detail="Удаление пользователей запрещено!"
    )

@router.post("/auth/jwt/refresh",tags=['auth'])
async def refresh_token(refresh_token: str): #pylint: disable=W0621
    """Эндпоинт для получения нового токена"""
    new_access_token = await auth_backend.transport.get_login_response(refresh_token)
    return {"access_token": new_access_token}
