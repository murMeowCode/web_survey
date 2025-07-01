"""Эндпоинты для внешней аутентификации"""
from fastapi import APIRouter, Depends, HTTPException
from nats.aio.client import Client as NATS
from sqlalchemy.ext.asyncio import AsyncSession
from main_auth.crud.oauth import get_or_create_oauth_user
from main_auth.schemas.oauth import GoogleAuthRequest, OAuthUserResponse
from main_auth.core.nats_utils import request_oauth_verification, get_nats_client
from main_auth.core.jwt_logic import create_access_token, create_refresh_token
from main_auth.core.database import get_async_session

router = APIRouter(prefix="/oauth")

@router.post("/google")
async def auth_via_google(
    request: GoogleAuthRequest,
    nats: NATS = Depends(get_nats_client),
    session: AsyncSession = Depends(get_async_session)
):
    """Аутентификация через Гугл"""
    oauth_data = await request_oauth_verification(
        nats, "google", {"token": request.token}
    )

    if not oauth_data.get("success"):
        raise HTTPException(400, "Google OAuth failed")

    user_data = OAuthUserResponse(**oauth_data["user"])

    user = await get_or_create_oauth_user(session=session,oauth_user=user_data)

    return {
        "access_token": create_access_token(user),
        "refresh_token": create_refresh_token(user)
    }
