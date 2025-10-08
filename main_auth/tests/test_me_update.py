"""модуль тестов для patch /users/me"""
import unittest
from fastapi.testclient import TestClient  # Используем синхронный TestClient
from fastapi import status
from main_auth.main import app
from main_auth.models.user import User

class TestUpdateMeEndpoint(unittest.TestCase):  # Используем обычный TestCase
    """Тестирование эндпоинта изменения пользователя"""
    def setUp(self):
        self.client = TestClient(app)  # Синхронный клиент
        self.test_user = User(
            id=1,
            email="old@example.com",
            is_active=True
        )

    def test_update_no_auth(self):
        """Попытка изменения без аутентификации"""
        response = self.client.patch(
            "/users/me",
            json={"email": "new@example.com"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
