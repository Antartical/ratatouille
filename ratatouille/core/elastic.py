import typing
import elasticsearch_dsl


MODEL = typing.TypeVar("MODEL", bound="Model")

Document = elasticsearch_dsl.Document
fields = elasticsearch_dsl


class ESIndex:
    """Baseclass for indexed models."""

    Document: elasticsearch_dsl.Document
    _index_id: str

    @classmethod
    def _search(cls: typing.Type[MODEL]) -> elasticsearch_dsl.Search:
        return cls.Document.search()

    @classmethod
    def es_search(
        cls: typing.Type[MODEL],
        query: str,
        fields: typing.Optional[typing.List[str]] = None,
        offset=0,
        limit=30
    ) -> elasticsearch_dsl.response.Response:
        """Multi match search for the given query.

        Args:
            query (str): query string. It can contains wildcards.
            fields (List[str], optional): the fields the search will be
                executed for, if it is none the search will be executed over
                all indexed fields. Defaults to None
            offset (int, optional): offset. Defaults to 0.
            limit (int, optional): limit results. Defaults to 30.

        Returns:
            elasticsearch_dsl.response.Response: elasticsearch response with
                matched hits.
        """
        fields = fields or []
        return cls._search()[offset:limit+offset].query(
            'query_string', query=query, fields=fields
        ).execute()

    @classmethod
    def es_match(
        cls: typing.Type[MODEL], attr: str, query: str, offset=0, limit=30
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

    @classmethod
    def destroy_index(cls: typing.Type[MODEL]) -> typing.Dict:
        """Removes the whole index and data."""
        return cls.Document._index.delete(ignore=404)

    @classmethod
    def build_index(cls: typing.Type[MODEL]):
        """Builds the index if it has not been created before."""
        cls.Document.init()

    @property
    def _get_doc_instance(self) -> typing.Optional[elasticsearch_dsl.Document]:
        if self._index_id:
            return self.Document.get(id=self._index_id)
        return None

    @property
    def to_document(self) -> typing.Dict:
        """Prepare the data to be indexed in the model.

        This method should return a dict with the keys and values of the fields
        the document will index.

        Returns:
            typing.Dict: the thada will be indexed by the document
        """

    def index(self) -> str:
        """Index the model into elastic.

        Returns:
          str: the id index of the indexed document
        """

        if doc := self._get_doc_instance:
            doc.update(**self.to_document)
        else:
            doc = self.Document(**self.to_document)
            doc.save()
        return doc.meta['id']

    def unindex(self):
        """Removes the model from elastic."""
        if doc := self._get_doc_instance:
            doc.delete()
