"""Тесты эндпоинта me"""
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi import status
from jose import jwt
from main_auth.main import app
from main_auth.models.user import User
from main_auth.core.config import Settings

class TestMeEndpoints(unittest.IsolatedAsyncioTestCase):
    """Класс для теста эндпоинта"""
    def setUp(self):
        """Функция первичной настройки"""
        self.client = TestClient(app)
        self.test_user = User(
            id=1,
            email="test@example.com",
            is_active=True,
            hashed_password="hashed_test"
        )
        self.valid_token = self._create_test_token()

    def _create_test_token(self):
        """Служебная функция создания токена"""
        return jwt.encode({
            "sub": "1",
            "exp": datetime.now() + timedelta(minutes=30)
        }, Settings().secret_key, algorithm=Settings().algorithm)

    async def test_get_me_success(self):
        """Проверка успешного доступа"""
        with patch("main_auth.api.users.get_current_user") as mock_get_user:
            mock_get_user.return_value = self.test_user

            response = self.client.get(
                "/me",
                headers={"Authorization": f"Bearer {self.valid_token}"}
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()["email"], "test@example.com")

    async def test_get_me_unauthorized(self):
        """Тест с неавторизованным доступом"""
        response = self.client.get("/me")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    async def test_get_me_invalid_token(self):
        """Тест с некорректным токеном"""
        response = self.client.get(
            "/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
