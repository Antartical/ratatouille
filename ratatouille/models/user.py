from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

from ratatouille.common import models


class User(models.UUIDTimestampedModel):
    """User model"""

    email = fields.CharField(max_length=244, null=True, unique=True)
    name = fields.CharField(max_length=50)
    surname = fields.CharField(max_length=50)
    birthday = fields.DateField()
    phone = fields.CharField(max_length=50)

    class Meta:
        table = 'user'


PUser = pydantic_model_creator(User, name='User')
