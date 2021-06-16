from unittest import mock, TestCase
from ratatouille.common import elastic


class ElasticTest(TestCase):

    class MockESIndex(elastic.ESIndex):
        Document = mock.MagicMock()
        _index_id = 1

    def test_search(self):
        mock_index = self.MockESIndex()
        mock_index._search()
        mock_index.Document.search.assert_called_once()

    def test_es_search(self):
        mock_index = self.MockESIndex()
        query = 'fake query'
        fields = []
        query_type = 'query_string'

        with mock.patch(
            'ratatouille.common.elastic.ESIndex._search', autospec=True
        ) as mock_search:
            mock_index.es_search(query)
            mock_search.assert_called_once()
            mock_search()[:].query.assert_called_once_with(
                query_type, query=query, fields=fields
            )

    def test_es_match(self):
        mock_index = self.MockESIndex()
        attr = 'fake_attr'
        query = 'fake query'
        query_type = 'match'

        with mock.patch(
            'ratatouille.common.elastic.ESIndex._search',
            autospec=True
        ) as mock_search:
            mock_index.es_match(attr, query)
            mock_search.assert_called_once()
            mock_search()[:].query.assert_called_once_with(
                query_type, **{attr: query}
            )

    def test_destroy_index(self):
        mock_index = self.MockESIndex()
        mock_index.destroy_index()
        mock_index.Document._index.delete.assert_called_once()

    def test_build_index(self):
        mock_index = self.MockESIndex()
        mock_index.build_index()
        mock_index.Document.init.assert_called_once()

    def test_get_doc_index(self):
        mock_index = self.MockESIndex()
        mock_index._get_doc_instance
        mock_index.Document.get.assert_called_once_with(
            id=mock_index._index_id)

    def test_get_doc_index_none(self):
        mock_index = self.MockESIndex()
        mock_index._index_id = None
        self.assertIsNone(mock_index._get_doc_instance)

    def test_index(self):
        mock_to_document = {
            'fake': 'fake'
        }
        mock_index = self.MockESIndex()
        mock_index._index_id = None

        with mock.patch(
            'ratatouille.common.elastic.ESIndex.to_document',
            return_value=mock_to_document
        ):
            mock_index.index()
            mock_index.Document().save.assert_called_once()

    def test_index_update(self):
        mock_to_document = {
            'fake': 'fake'
        }
        mock_index = self.MockESIndex()

        with mock.patch(
            'ratatouille.common.elastic.ESIndex.to_document',
            return_value=mock_to_document
        ), \
            mock.patch(
            'ratatouille.common.elastic.ESIndex._get_doc_instance'
        ) as mock_doc_instance:
            mock_index.index()
            mock_doc_instance.update.assert_called_once()

    def test_unindex(self):
        mock_index = self.MockESIndex()

        with mock.patch(
            'ratatouille.common.elastic.ESIndex._get_doc_instance'
        ) as mock_doc_instance:
            mock_index.unindex()
            mock_doc_instance.delete.assert_called_once()
