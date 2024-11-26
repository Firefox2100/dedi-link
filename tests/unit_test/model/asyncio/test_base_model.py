import pytest
from enum import Enum

from dedi_link.etc.exceptions import BaseModelNotImplemented
from dedi_link.model.asyncio import AsyncBaseModel


class TestAsyncBaseModel:
    @pytest.mark.asyncio
    async def test_access_token(self):
        base_model_instance = AsyncBaseModel()
        with pytest.raises(BaseModelNotImplemented):
            _ = await base_model_instance.access_token

    @pytest.mark.asyncio
    async def test_load(self):
        with pytest.raises(BaseModelNotImplemented):
            await AsyncBaseModel.load()

    @pytest.mark.asyncio
    async def test_load_all(self):
        with pytest.raises(BaseModelNotImplemented):
            await AsyncBaseModel.load_all()

    @pytest.mark.asyncio
    async def test_store(self):
        base_model_instance = AsyncBaseModel()
        with pytest.raises(BaseModelNotImplemented):
            await base_model_instance.store()

    @pytest.mark.asyncio
    async def test_update(self):
        base_model_instance = AsyncBaseModel()
        with pytest.raises(BaseModelNotImplemented):
            await base_model_instance.update({})

    @pytest.mark.asyncio
    async def test_delete(self):
        base_model_instance = AsyncBaseModel()
        with pytest.raises(BaseModelNotImplemented):
            await base_model_instance.delete()

    def test_to_dict(self):
        base_model_instance = AsyncBaseModel()
        with pytest.raises(BaseModelNotImplemented):
            base_model_instance.to_dict()

    def test_from_dict(self):
        with pytest.raises(BaseModelNotImplemented):
            AsyncBaseModel.from_dict({})

    def test_factory_from_id_with_no_mapping(self):
        class TestEnum(Enum):
            TEST = 'test'
            ANOTHER_TEST = 'another_test'

        with pytest.raises(BaseModelNotImplemented):
            AsyncBaseModel.factory_from_id({}, TestEnum.TEST)

    def test_factory_from_id_mapping_not_exist(self):
        class TestEnum(Enum):
            TEST = 'test'
            ANOTHER_TEST = 'another_test'

        class TestModel(AsyncBaseModel):
            @classmethod
            def _child_mapping(cls):
                return {
                    TestEnum.TEST: (TestModel, None),
                }

        with pytest.raises(ValueError):
            TestModel.factory_from_id({}, TestEnum.ANOTHER_TEST)

    def test_factory(self):
        with pytest.raises(BaseModelNotImplemented):
            AsyncBaseModel.factory({})
