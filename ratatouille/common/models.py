"""This module contains common abstract models.

All of those are compatible with Tortoise ORM
"""


import typing
import logging
import elasticsearch_dsl
from uuid import uuid4
from tortoise import fields, models
from tortoise.queryset import QuerySet


from ratatouille.common.elastic import ESIndex


logger = logging.getLogger(__name__)


MODEL = typing.TypeVar("MODEL", bound="Model")


class IndexedModel(models.Model, ESIndex):
    """IndexedModel.

    This model will index the document into elastic for search queries.
    """

    _index_id = fields.CharField(max_length=255, null=True, unique=True)

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

    @classmethod
    def _covert_es_response_to_queryset(
        cls: typing.Type[MODEL],
        es_response: elasticsearch_dsl.response.Response
    ) -> QuerySet[MODEL]:
        """Converts es matched data to tortoise ORM queryset.

        Args:
            es_response (elasticsearch_dsl.response.Response): elasticsearch
                match response.

        Returns:
            QuerySet[Model]: converted es response.
        """
        indexed_ids = [hit.meta['id'] for hit in es_response.hits]
        return cls.filter(_index_id__in=indexed_ids)

    @classmethod
    def search(
        cls: typing.Type[MODEL], query: str, offset=0, limit=30
    ) -> QuerySet[MODEL]:
        """Multi match search for the given query.

        This method will match the query agains ES and obtains the queryset
        from the tortoise database by querying their ids.

        Args:
            query (str): es query string. It can contains wildcards.
            offset (int, optional): offset. Defaults to 0.
            limit (int, optional): limit results. Defaults to 30.

        Returns:
            Queryset[MODEL]: a queryset with the matched records.
        """
        return cls._covert_es_response_to_queryset(
            cls.es_search(query, offset, limit)
        )

    @classmethod
    def match(
        cls: typing.Type[MODEL], attr: str, query: str, offset=0, limit=30
    ) -> QuerySet[MODEL]:
        """Match exact query for the given attribute name.

        This method will match the query agains ES and obtains the queryset
        from the tortoise database by querying their ids.

        Args:
            attr (str): attr name.
            query (str): query string. It cannot contains wildcards.
            offset (int, optional): offset. Defaults to 0.
            limit (int, optional): limit results. Defaults to 30.

        Returns:
            Queryset[MODEL]: a queryset with the matched records.
        """
        return cls._covert_es_response_to_queryset(
            cls.es_match(attr, query, offset, limit)
        )

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
