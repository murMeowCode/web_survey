"""Эндпоинты для информации о пользователе"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from main_auth.core.database import get_async_session
from main_auth.core.jwt_logic import get_current_user
from main_auth.crud.user import update_user_info
from main_auth.schemas.user import UserRead, UserUpdate
from main_auth.models.user import User

router = APIRouter(prefix='/users',tags=['users'])

@router.get('/me',response_model=UserRead)
async def get_my_info(current_user: User = Depends(get_current_user)):
    """Получение информации о себе"""
    return current_user

@router.patch('/me',response_model=UserRead)
async def change_personal_info(new_data : UserUpdate,
                               current_user: User = Depends(get_current_user),
                               session : AsyncSession = Depends(get_async_session)):
    """Изменение своих личных данных"""
    new_info = await update_user_info(new_data=new_data,
                                      current_user=current_user,
                                      session=session)
    return new_info
