"""Тесты для update me"""
from datetime import datetime,timedelta
import unittest
from unittest.mock import AsyncMock, patch
import jwt
from fastapi.testclient import TestClient
from fastapi import status
from main_auth.main import app
from main_auth.models.user import User
from main_auth.core.config import Settings

class TestUpdateMeEndpoint(unittest.IsolatedAsyncioTestCase):
    """Тесты изменения информации"""
    def setUp(self):
        """Первичная настройка"""
        self.client = TestClient(app)
        self.test_user = User(
            id=1,
            email="old@example.com",
            is_active=True
        )
        self.valid_token = self._create_test_token()

    def _create_test_token(self):
        """Служебная функция для создания токена"""
        return jwt.encode({
            "sub": "1",
            "exp": datetime.now() + timedelta(minutes=30)
        }, Settings().secret_key, algorithm=Settings().algorithm)

    @patch("api.users.get_current_user")
    @patch("api.users.get_async_session")
    async def test_update_email_success(self, mock_get_session, mock_get_user):
        """Тест успешной смены почты"""
        # Setup mocks
        mock_get_user.return_value = self.test_user
        mock_session = AsyncMock()
        mock_get_session.return_value = mock_session

        # Mock database operations
        mock_session.__aenter__.return_value = mock_session
        mock_session.commit = AsyncMock()
        mock_session.refresh = AsyncMock()

        response = self.client.patch(
            "/me",
            json={"email": "new@example.com"},
            headers={"Authorization": f"Bearer {self.valid_token}"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["email"], "new@example.com")
        mock_session.commit.assert_awaited_once()

    @patch("api.users.get_current_user")
    async def test_update_password(self, mock_get_user):
        """Тест изменения пароля"""
        mock_get_user.return_value = self.test_user

        with patch("api.users.get_password_hash") as mock_hash:
            mock_hash.return_value = "new_hashed_password"

            response = self.client.patch(
                "/me",
                json={"password": "new_password"},
                headers={"Authorization": f"Bearer {self.valid_token}"}
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            mock_hash.assert_called_once_with("new_password")

    async def test_update_no_auth(self):
        """Попытка изменения без аутентификации"""
        response = self.client.patch("/me", json={"email": "new@example.com"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
