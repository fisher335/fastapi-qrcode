from sqlite3 import IntegrityError

from fastapi import HTTPException
from tortoise.exceptions import DoesNotExist

from database.model.models import Users, Device
from database.schemas.common import Status
from database.schemas.device import DevOutSchema


async def create_dev(DevInSchema) -> DevOutSchema:
    try:
        user_obj = await Users.create(**DevInSchema.dict(exclude_unset=True))
    except IntegrityError:
        raise HTTPException(status_code=401, detail=f"Sorry, that dev already exists.")

    return await DevOutSchema.from_tortoise_orm(user_obj)


async def delete_dev(dev_id, current_user) -> Status:
    try:
        db_dev = await DevOutSchema.from_queryset_single(Device.get(id=dev_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"dev {dev_id} not found")

    if db_dev:
        deleted_count = await Device.filter(id=dev_id).delete()
        if not deleted_count:
            raise HTTPException(status_code=404, detail=f"dev {dev_id} not found")
        return Status(message=f"Deleted user {dev_id}")

    raise HTTPException(status_code=403, detail=f"Not authorized to delete")


async def update_dev(dev_id, dev) -> DevOutSchema:
    try:
        db_note = await DevOutSchema.from_queryset_single(Device.get(id=dev_id))
    except DoesNotExist:
        raise HTTPException(status_code=404, detail=f"dev {dev_id} not found")

    if db_note:
        await Device.filter(id=dev_id).update(**dev.dict(exclude_unset=True))
        return await DevOutSchema.from_queryset_single(Device.get(id=dev_id))

    raise HTTPException(status_code=403, detail=f"Not authorized to update")


async def get_devs():
    return await DevOutSchema.from_queryset(Device.all())


async def get_dev(dev_id) -> Users:
    return await DevOutSchema.from_queryset_single(Device.get(id=dev_id))
