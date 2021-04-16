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
    """IndexedModel."""

    _index_id = fields.CharField(max_length=255, null=True, unique=True)

    @classmethod
    def _convert_es_response_to_queryset(
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
        cls: typing.Type[MODEL],
        query: str,
        fields: typing.Optional[typing.List[str]] = None,
        offset: int = 0,
        limit: int = 30
    ) -> QuerySet[MODEL]:
        """Multi match search for the given query.

        This method will match the query agains ES and obtains the queryset
        from the tortoise database by querying their ids.

        Args:
            query (str): es query string. It can contains wildcards.
            fields (List[str], optional): the fields the search will be
                executed for, if it is none the search will be executed over
                all indexed fields. Defaults to None
            offset (int, optional): offset. Defaults to 0.
            limit (int, optional): limit results. Defaults to 30.

        Returns:
            Queryset[MODEL]: a queryset with the matched records.
        """
        return cls._convert_es_response_to_queryset(
            cls.es_search(query, fields, offset, limit)
        )

    @classmethod
    def match(
        cls: typing.Type[MODEL],
        query: str,
        field: str,
        offset: int = 0,
        limit: int = 30
    ) -> QuerySet[MODEL]:
        """Match exact query for the given attribute name.

        This method will match the query agains ES and obtains the queryset
        from the tortoise database by querying their ids.

        Args:
            query (str): query string. It cannot contains wildcards.
            field (str): attr name.
            offset (int, optional): offset. Defaults to 0.
            limit (int, optional): limit results. Defaults to 30.

        Returns:
            Queryset[MODEL]: a queryset with the matched records.
        """
        return cls._convert_es_response_to_queryset(
            cls.es_match(field, query, offset, limit)
        )

    async def save(self, *args, **kwargs):
        if '_index_id' not in kwargs.get('update_fields', []):
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
