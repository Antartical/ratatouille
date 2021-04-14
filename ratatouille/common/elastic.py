import typing
import elasticsearch_dsl


class DocumentError(Exception):
    """
    This exception will be raised whether there are more
    than one matched doc.
    """


class ESIndex:
    """Baseclass for indexed models."""

    Document: elasticsearch_dsl.Document
    _index_id: str

    class Meta:
        indexed_fields = []

    @classmethod
    def search(cls) -> elasticsearch_dsl.Search:
        return cls.Document.search()

    @property
    def _get_doc_instance(self) -> typing.Optional[elasticsearch_dsl.Document]:
        if self._index_id:
            return self.Document.get(id=self._index_id)
        return None

    def index(self) -> str:
        """Index the model into elastic.

        Returns:
          str: the id index of the indexed document
        """
        data = {attr: getattr(self, attr) for attr in self.Meta.indexed_fields}
        if doc := self._get_doc_instance:
            doc = self._get_doc_instance
            for attr in self.Meta.indexed_fields:
                setattr(doc, attr, getattr(self, attr))
            doc.update(**data)
        else:
            doc = self.Document(**data)
            doc.save()
        return doc.meta['id']

    @classmethod
    def destroy_index(cls) -> typing.Dict:
        """Removes the whole index and data."""
        return cls.Document._index.delete(ignore=404)

    @classmethod
    def build_index(cls):
        """Builds the index if it has not been created before."""
        cls.Document.init()
