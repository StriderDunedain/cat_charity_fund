from fastapi import APIRouter

from app.core.user import auth_backend, fastapi_users
from app.schemas.user import UserCreate, UserRead, UserUpdate

user_router = APIRouter()

user_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
user_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)

users_router = fastapi_users.get_users_router(UserRead, UserUpdate)
# Из списка эндпоинтов роутера исключаем ненужную ручку.
users_router.routes = [
    rout for rout in users_router.routes if rout.name != 'users:delete_user'
]
# Подключаем изменённый роутер по старому адресу.
user_router.include_router(
    users_router,
    prefix='/users',
    tags=['users'],
)
