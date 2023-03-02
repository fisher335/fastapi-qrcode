from sqlite3 import IntegrityError

from fastapi import HTTPException
from passlib.context import CryptContext
from tortoise.exceptions import DoesNotExist

from database.model.models import Users
from database.schemas.common import Status
from database.schemas.users import UserOutSchema, UserDatabaseSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def create_user(user) -> UserOutSchema:
    user.password = pwd_context.encrypt(user.login_name)

    try:
        user_obj = await Users.create(**user.dict(exclude_unset=True))
    except IntegrityError:
        raise HTTPException(status_code=401, detail=f"Sorry, that username already exists.")

    return await UserOutSchema.from_tortoise_orm(user_obj)


async def delete_user(user_id, current_user) -> Status:
    try:
        db_user = await UserOutSchema.from_queryset_single(Users.get(id=user_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")

    if db_user.id == current_user.id:
        deleted_count = await Users.filter(id=user_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"User {user_id} not found")
        return Status(message=f"Deleted user {user_id}")

    raise HTTPException(status_code=403, detail=f"Not authorized to delete")


async def get_users():
    return await UserOutSchema.from_queryset(Users.all())


async def get_user_password(user_id) -> Users:
    return await UserDatabaseSchema.from_queryset_single(Users.get(login_name=user_id))


async def get_user(user_id) -> Users:
    return await UserOutSchema.from_queryset_single(Users.get(login_name=user_id))


async def query_users(user_id) -> Users:
    return await UserOutSchema.from_queryset(Users.filter(login_name__contains=user_id))


async def update_user(user) -> UserOutSchema:
    try:
        db_note = await UserOutSchema.from_queryset_single(Users.get(login_name=user.login_name))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"userid  {user.login_name} not found")

    if db_note:
        await Users.filter(login_name=user.user_id).update(**user.dict(exclude_unset=True))
        return await UserOutSchema.from_queryset_single(Users.get(login_name=user.login_name))

    raise HTTPException(status_code=403, detail=f"Not authorized to update")
