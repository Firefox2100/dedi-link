import pytest
from enum import Enum

from dedi_link.etc.exceptions import BaseModelNotImplemented
from dedi_link.model import BaseModel, SyncDataInterface


class TestSyncDataInterface:
    def test_load(self):
        with pytest.raises(BaseModelNotImplemented):
            SyncDataInterface.load()

    def test_load_all(self):
        with pytest.raises(BaseModelNotImplemented):
            SyncDataInterface.load_all()

    def test_store(self):
        sync_interface_instance = SyncDataInterface()
        with pytest.raises(BaseModelNotImplemented):
            sync_interface_instance.store()

    def test_update(self):
        sync_interface_instance = SyncDataInterface()
        with pytest.raises(BaseModelNotImplemented):
            sync_interface_instance.update({})

    def test_delete(self):
        sync_interface_instance = SyncDataInterface()
        with pytest.raises(BaseModelNotImplemented):
            sync_interface_instance.delete()


class TestBaseModel:
    def test_access_token(self):
        base_model_instance = BaseModel()
        with pytest.raises(ValueError):
            _ = base_model_instance.access_token

    def test_to_dict(self):
        base_model_instance = BaseModel()
        with pytest.raises(BaseModelNotImplemented):
            base_model_instance.to_dict()

    def test_from_dict(self):
        with pytest.raises(BaseModelNotImplemented):
            BaseModel.from_dict({})

    def test_factory_from_id_with_no_mapping(self):
        class TestEnum(Enum):
            TEST = 'test'
            ANOTHER_TEST = 'another_test'

        with pytest.raises(AttributeError):
            BaseModel.factory_from_id({}, TestEnum.TEST)

    def test_factory_from_id(self):
        class TestEnum(Enum):
            PARENT = 'parent'
            CHILD = 'child'

        class TestParent(BaseModel):
            child_registry = {}

        @TestParent.register_child(TestEnum.CHILD)
        class TestChild(TestParent):
            @classmethod
            def from_dict(cls, payload):
                pass

        _ = TestParent.factory_from_id({}, TestEnum.CHILD)

    def test_factory(self):
        with pytest.raises(BaseModelNotImplemented):
            BaseModel.factory({})
