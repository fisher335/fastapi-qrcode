
from tortoise.contrib.pydantic import pydantic_model_creator

from database.model.models import Users

UserInSchema = pydantic_model_creator(
    Users, name="UserIn", exclude_readonly=True,exclude=["id"]
)
UserOutSchema = pydantic_model_creator(
    Users, name="UserOut", exclude=["password", "created_at", "modified_at"]
)
UserDatabaseSchema = pydantic_model_creator(
    Users, name="User"
)

