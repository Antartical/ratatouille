import typing
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

from ratatouille.core import models, elastic


class User(models.UUIDTimestampedModel, models.IndexedModel):
    """User model"""

    email = fields.CharField(max_length=244, null=True, unique=True)
    name = fields.CharField(max_length=50)
    surname = fields.CharField(max_length=50)
    birthday = fields.DateField()
    phone = fields.CharField(max_length=50)

    class Document(elastic.Document):
        id = elastic.fields.Keyword()
        uuid = elastic.fields.Keyword()
        email = elastic.fields.Keyword()
        name = elastic.fields.Text()

        class Index:
            name = 'user'

    @property
    def to_document(self) -> typing.Dict:
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
