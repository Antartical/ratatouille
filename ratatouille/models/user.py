import typing
import elasticsearch_dsl
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

from ratatouille.common import models


class User(models.UUIDTimestampedModel, models.IndexedModel):
    """User model"""

    email = fields.CharField(max_length=244, null=True, unique=True)
    name = fields.CharField(max_length=50)
    surname = fields.CharField(max_length=50)
    birthday = fields.DateField()
    phone = fields.CharField(max_length=50)

    class Document(elasticsearch_dsl.Document):
        id = elasticsearch_dsl.Keyword()
        uuid = elasticsearch_dsl.Keyword()
        email = elasticsearch_dsl.Keyword()
        name = elasticsearch_dsl.Text()

        class Index:
            name = 'user'

    def prepare(self) -> typing.Dict:
        """Return dict with the data that will be indexed"""
        return {
            'id': self.id,
            'uuid': self.uuid,
            'email': self.email,
            'name': self.name
        }

    class Meta:
        table = 'user'


PUser = pydantic_model_creator(User, name='User')
