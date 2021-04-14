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
    def _search(cls) -> elasticsearch_dsl.Search:
        return cls.Document.search()

    @classmethod
    def search(
        cls, query, offset=0, limit=30
    ) -> elasticsearch_dsl.response.Response:
        """Multi match search for the given query.

        Args:
            query (str): query string. It can contains wildcards.
            offset (int, optional): offset. Defaults to 0.
            limit (int, optional): limit results. Defaults to 30.

        Returns:
            elasticsearch_dsl.response.Response: elasticsearch response with
                matched hits.
        """
        return cls._search()[offset:limit+offset].query(
            'query_string', query=query, fields=cls.Meta.indexed_fields
        ).execute()

    @classmethod
    def match(
        cls, attr: str, query: str, offset=0, limit=30
    ) -> elasticsearch_dsl.response.Response:
        """Match exact query for the given attribute name.

        Args:
            attr (str): attr name.
            query (str): query string. It cannot contains wildcards.
            offset (int, optional): offset. Defaults to 0.
            limit (int, optional): limit results. Defaults to 30.

        Returns:
            elasticsearch_dsl.response.Response: [description]
        """
        return cls._search()[offset:limit+offset].query(
            'match', **{attr: query}
        ).execute()

    @ classmethod
    def destroy_index(cls) -> typing.Dict:
        """Removes the whole index and data."""
        return cls.Document._index.delete(ignore=404)

    @ classmethod
    def build_index(cls):
        """Builds the index if it has not been created before."""
        cls.Document.init()

    @ property
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
