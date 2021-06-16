from unittest import mock
from ratatouille.common import test, models


class IndexedModelTest(test.AsyncAbstractModelTestCase):

    class Model(models.IndexedModel):
        id = 1
        _index_id = 1
        Document = mock.MagicMock()
        to_document = {'id': 1}

    async def test_convert_es_response_to_queryset(self):
        hit_id = 1
        hit = mock.Mock(meta={'id': hit_id})
        es_response = mock.Mock(hits=[hit])

        expected_ids_args = [hit_id]
        model = await self.get_model()
        model._convert_es_response_to_queryset(es_response)
        model.filter.assert_called_once_with(_index_id__in=expected_ids_args)

    async def test_search(self):
        query = 'fake query'

        model = await self.get_model()
        with mock.patch.object(self.Model, 'es_search') as mock_es_search:
            model.search(query, offset=0, limit=30)
            mock_es_search.assert_called_once_with(query, None, 0, 30)

    async def test_match(self):
        query = 'fake query'
        field = 'fake field'

        model = await self.get_model()
        with mock.patch.object(self.Model, 'es_match') as mock_es_match:
            model.match(field, query, offset=0, limit=30)
            mock_es_match.assert_called_once_with(query, field, 0, 30)

    async def test_save_with_pk(self):
        model = await self.get_model()
        with mock.patch('tortoise.models.Model.save') as mock_super_save, \
                mock.patch.object(model, 'index') as mock_index:
            await model.save()

            mock_super_save.assert_called_once()
            mock_index.assert_called_once()

    async def test_save_without_pk(self):
        model = await self.get_model()
        with mock.patch('tortoise.models.Model.save') as mock_super_save, \
                mock.patch.object(model, 'index') as mock_index:
            reset = type(model).pk
            type(model).pk = mock.PropertyMock(side_effect=[None, 1])
            await model.save()

            mock_index.assert_called_once()
            self.assertEqual(mock_super_save.call_count, 2)
            type(model).pk = reset

    async def test_delete(self):
        model = await self.get_model()
        with mock.patch('tortoise.models.Model.delete') as mock_super_delete, \
                mock.patch.object(model, 'unindex') as mock_unindex:
            await model.delete()

            mock_unindex.assert_called_once()
            mock_super_delete.assert_called_once()
