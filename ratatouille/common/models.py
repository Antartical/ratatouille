"""This module contains common abstract models.

All of those are compatible with Tortoise ORM
"""


import logging
from uuid import uuid4
from tortoise import fields, models


from ratatouille.common.elastic import ESIndex


logger = logging.getLogger(__name__)


class IndexedModel(models.Model, ESIndex):
    """IndexedModel.

    This model will index the document into elastic for search queries.
    """

    _index_id = fields.CharField(max_length=255, null=True)

    @classmethod
    async def rebuild_index(cls):
        logging.info(f'Rebuild index {cls.Document.Index.name}')
        cls.destroy_index()
        cls.build_index()

        total_objects = await cls.all().count()
        count = 0
        async for obj in cls.all():
            obj._index_id = None
            obj._index_id = obj.index()
            await obj.save(update_fields=['_index_id'])
            count += 1
            if count % 500 == 0:
                logging.info(f' Indexed: {count} of {total_objects}')

        logging.info(f'Indexed {cls.Document.Index.name} successfully rebuild')

    async def save(self, *args, **kwargs):
        self._index_id = self.index()
        await super().save(*args, **kwargs)

    class Meta:
        abstract = True


class UUIDTimestampedModel(models.Model):
    """UUIDTimestampedModel

    This model provides:
        - id
        - uuid
        - created_at
        - modified_at
    """

    id = fields.IntField(pk=True)
    uuid = fields.UUIDField(default=uuid4, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True
