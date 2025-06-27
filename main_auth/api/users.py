"""Эндпоинты для информации о пользователе"""
from fastapi import APIRouter

router = APIRouter(prefix='/users',tags=['users'])
