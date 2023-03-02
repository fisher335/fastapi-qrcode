from typing import Optional

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from database.model.models import Device

DevInSchema = pydantic_model_creator(
    Device, name="DevIn", exclude_readonly=True,exclude=["id"]
)
DevOutSchema = pydantic_model_creator(
    Device, name="DevOut"
)
DevDatabaseSchema = pydantic_model_creator(
    Device, name="Device"
)

