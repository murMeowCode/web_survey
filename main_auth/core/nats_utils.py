#pylint: disable=W0707
"""Инструменты для работы с NATS"""
import json
import asyncio
from nats.aio.client import Client as NATS
from fastapi import HTTPException
from main_auth.core.config import Settings

class NATSClient:
    """Класс для работы с соединением"""
    def __init__(self):
        self._client = None
        self._connect_lock = asyncio.Lock()

    async def connect(self):
        """Соединение с сервером"""
        if self._client is None or self._client.is_closed:
            async with self._connect_lock:
                if self._client is None or self._client.is_closed:
                    self._client = NATS()
                    await self._client.connect(
                        servers=[Settings().nats_url],
                        connect_timeout=5,
                        max_reconnect_attempts=3
                    )
        return self._client

    async def close(self):
        """Закрытие соединения"""
        if self._client and not self._client.is_closed:
            await self._client.close()

nats_client = NATSClient()

async def get_nats_client() -> NATS:
    """Dependency для получения NATS подключения"""
    return await nats_client.connect()

async def on_shutdown():
    """Закрытие соединения при завершении приложения"""
    await nats_client.close()

async def request_oauth_verification(
    nats: NATS,
    provider: str,
    data: dict
) -> dict:
    """Получение данных пользователя от провайдера"""
    try:
        response = await nats.request(
            f"oauth.{provider}",
            json.dumps(data).encode(),
            timeout=3.0
        )
        return json.loads(response.data)
    except Exception as e:
        raise HTTPException(504, f"OAuth service error: {str(e)}")
