import pytest

from dedi_link.etc.exceptions import BaseModelNotImplemented
from dedi_link.model.asyncio import AsyncBaseModel


@pytest.mark.asyncio
class TestAsyncBaseModel:
    async def test_load(self):
        with pytest.raises(BaseModelNotImplemented):
            await AsyncBaseModel.load()

    async def test_load_all(self):
        with pytest.raises(BaseModelNotImplemented):
            await AsyncBaseModel.load_all()

    async def test_store(self):
        base_model_instance = AsyncBaseModel()
        with pytest.raises(BaseModelNotImplemented):
            await base_model_instance.store()

    async def test_update(self):
        base_model_instance = AsyncBaseModel()
        with pytest.raises(BaseModelNotImplemented):
            await base_model_instance.update({})

    async def test_delete(self):
        base_model_instance = AsyncBaseModel()
        with pytest.raises(BaseModelNotImplemented):
            await base_model_instance.delete()
