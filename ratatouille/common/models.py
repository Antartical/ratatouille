"""This module contains common abstract models.

All of those are compatible with Tortoise ORM
"""


from uuid import uuid4
from tortoise import fields, models


class UUIDTimestampedModel(models.Model):
    """UUIDTimestampedModel

    This model provides:
        - id
        - uuid
        - created_at
        - modified_at
    """

    id = fields.IntField(pk=True)
    uuid = fields.UUIDField(default=uuid4)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True
