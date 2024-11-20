import pytest
from enum import Enum

from dedi_link.etc.exceptions import BaseModelNotImplemented
from dedi_link.model import BaseModel


class TestBaseModel:
    def test_load(self):
        with pytest.raises(BaseModelNotImplemented):
            BaseModel.load()

    def test_load_all(self):
        with pytest.raises(BaseModelNotImplemented):
            BaseModel.load_all()

    def test_store(self):
        base_model_instance = BaseModel()
        with pytest.raises(BaseModelNotImplemented):
            base_model_instance.store()

    def test_update(self):
        base_model_instance = BaseModel()
        with pytest.raises(BaseModelNotImplemented):
            base_model_instance.update({})

    def test_delete(self):
        base_model_instance = BaseModel()
        with pytest.raises(BaseModelNotImplemented):
            base_model_instance.delete()

    def test_to_dict(self):
        base_model_instance = BaseModel()
        with pytest.raises(BaseModelNotImplemented):
            base_model_instance.to_dict()

    def test_from_dict(self):
        with pytest.raises(BaseModelNotImplemented):
            BaseModel.from_dict({})

    def test_factory_with_no_mapping(self):
        class TestEnum(Enum):
            TEST = 'test'
            ANOTHER_TEST = 'another_test'

        with pytest.raises(BaseModelNotImplemented):
            BaseModel.factory({}, TestEnum.TEST)

    def test_factory_mapping_not_exist(self):
        class TestEnum(Enum):
            TEST = 'test'
            ANOTHER_TEST = 'another_test'

        class TestModel(BaseModel):
            @classmethod
            def _child_mapping(cls):
                return {
                    TestEnum.TEST: (TestModel, None),
                }

        with pytest.raises(ValueError):
            TestModel.factory({}, TestEnum.ANOTHER_TEST)
