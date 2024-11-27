import pytest

from dedi_link.etc.exceptions import BaseModelNotImplemented
from dedi_link.model.asyncio import AsyncDataInterface


@pytest.mark.asyncio
class TestAsyncDataInterface:
    async def test_access_token(self):
        async_interface_instance = AsyncDataInterface()
        with pytest.raises(BaseModelNotImplemented):
            _ = await async_interface_instance.access_token

    async def test_load(self):
        with pytest.raises(BaseModelNotImplemented):
            await AsyncDataInterface.load()

    async def test_load_all(self):
        with pytest.raises(BaseModelNotImplemented):
            await AsyncDataInterface.load_all()

    async def test_store(self):
        async_interface_instance = AsyncDataInterface()
        with pytest.raises(BaseModelNotImplemented):
            await async_interface_instance.store()

    async def test_update(self):
        async_interface_instance = AsyncDataInterface()
        with pytest.raises(BaseModelNotImplemented):
            await async_interface_instance.update({})

    async def test_delete(self):
        async_interface_instance = AsyncDataInterface()
        with pytest.raises(BaseModelNotImplemented):
            await async_interface_instance.delete()
