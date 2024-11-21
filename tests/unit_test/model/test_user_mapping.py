import pytest
from deepdiff import DeepDiff

from dedi_link.etc.enums import MappingType
from dedi_link.model import UserMapping


@pytest.fixture
def mock_user_mapping_1():
    return UserMapping(
        mapping_type=MappingType.STATIC,
        static_id='46592ab0-196a-4db2-a7fe-baf9a83d493b',
    )


@pytest.fixture
def mock_user_mapping_2():
    return UserMapping(
        mapping_type=MappingType.DYNAMIC,
        dynamic_mapping={
            'b6c2f7ca-95f5-4d00-94eb-dd289a000f7b': 'ed946072-57b9-4c00-a813-501773dc6146',
            '1303f0bc-0707-4118-97b5-7a5c9cfa9d8a': '0b5b32d0-317c-4d48-9874-8afddb913d08',
        },
    )


class TestUserMapping:
    def test_init(self):
        empty_mapping = UserMapping()

        assert empty_mapping.mapping_type == MappingType.NO_MAPPING
        assert empty_mapping.static_id is None
        assert empty_mapping.dynamic_mapping == {}

        static_mapping = UserMapping(
            mapping_type=MappingType.STATIC,
            static_id='46592ab0-196a-4db2-a7fe-baf9a83d493b',
        )

        assert static_mapping.mapping_type == MappingType.STATIC
        assert static_mapping.static_id == '46592ab0-196a-4db2-a7fe-baf9a83d493b'
        assert static_mapping.dynamic_mapping == {}

    def test_init_missing_static_id(self):
        with pytest.raises(ValueError):
            UserMapping(
                mapping_type=MappingType.STATIC,
            )

    def test_equality(self, mock_user_mapping_1, mock_user_mapping_2):
        assert mock_user_mapping_1 == UserMapping(
            mapping_type=MappingType.STATIC,
            static_id='46592ab0-196a-4db2-a7fe-baf9a83d493b',
        )

        # Static ID is different
        assert mock_user_mapping_1 != UserMapping(
            mapping_type=MappingType.STATIC,
            static_id='72196940-eb8d-409d-9bf9-0ce4b20a7751',
        )

        # Dynamic mapping is not compared in static type
        assert mock_user_mapping_1 == UserMapping(
            mapping_type=MappingType.STATIC,
            static_id='46592ab0-196a-4db2-a7fe-baf9a83d493b',
            dynamic_mapping={
                'b6c2f7ca-95f5-4d00-94eb-dd289a000f7b': 'ed946072-57b9-4c00-a813-501773dc6146',
                '1303f0bc-0707-4118-97b5-7a5c9cfa9d8a': '0b5b32d0-317c-4d48-9874-8afddb913d08',
            },
        )

        assert mock_user_mapping_1 != mock_user_mapping_2
        assert mock_user_mapping_1 != 'Random String'
        assert UserMapping(
            mapping_type='Wrong input',     # noqa
        ) != UserMapping(
            mapping_type='Wrong input',     # noqa
        )

    def test_to_dict(self, mock_user_mapping_1, mock_user_mapping_2):
        payload_1 = {
            'mappingType': 'static',
            'staticId': '46592ab0-196a-4db2-a7fe-baf9a83d493b',
        }

        payload_2 = {
            'mappingType': 'dynamic',
            'dynamicMapping': {
                'b6c2f7ca-95f5-4d00-94eb-dd289a000f7b': 'ed946072-57b9-4c00-a813-501773dc6146',
                '1303f0bc-0707-4118-97b5-7a5c9cfa9d8a': '0b5b32d0-317c-4d48-9874-8afddb913d08',
            },
        }

        assert not DeepDiff(
            mock_user_mapping_1.to_dict(),
            payload_1,
            ignore_order=True,
        )

        assert not DeepDiff(
            mock_user_mapping_2.to_dict(),
            payload_2,
            ignore_order=True,
        )

    def test_from_dict(self, mock_user_mapping_1, mock_user_mapping_2):
        payload_1 = {
            'mappingType': 'static',
            'staticId': '46592ab0-196a-4db2-a7fe-baf9a83d493b',
        }

        payload_2 = {
            'mappingType': 'dynamic',
            'dynamicMapping': {
                'b6c2f7ca-95f5-4d00-94eb-dd289a000f7b': 'ed946072-57b9-4c00-a813-501773dc6146',
                '1303f0bc-0707-4118-97b5-7a5c9cfa9d8a': '0b5b32d0-317c-4d48-9874-8afddb913d08',
            },
        }

        user_mapping_1 = UserMapping.from_dict(payload_1)
        user_mapping_2 = UserMapping.from_dict(payload_2)

        assert user_mapping_1 == mock_user_mapping_1
        assert user_mapping_2 == mock_user_mapping_2

    def test_map(self, mock_user_mapping_1, mock_user_mapping_2):
        # No mapping
        user_mapping = UserMapping()

        assert user_mapping.map('7c1cd6ae-8f35-4ce6-9631-d05901dc41bb') == '7c1cd6ae-8f35-4ce6-9631-d05901dc41bb'
        with pytest.raises(ValueError):
            # No-mapping type requires an original ID
            user_mapping.map()

        assert mock_user_mapping_1.map() == '46592ab0-196a-4db2-a7fe-baf9a83d493b'
        assert mock_user_mapping_1.map('7c1cd6ae-8f35-4ce6-9631-d05901dc41bb') == '46592ab0-196a-4db2-a7fe-baf9a83d493b'

        assert mock_user_mapping_2.map('b6c2f7ca-95f5-4d00-94eb-dd289a000f7b') == 'ed946072-57b9-4c00-a813-501773dc6146'
        with pytest.raises(ValueError):
            # Dynamic mapping requires an original ID
            mock_user_mapping_2.map()
        with pytest.raises(ValueError):
            # Original ID not in the LUT
            mock_user_mapping_2.map('7c1cd6ae-8f35-4ce6-9631-d05901dc41bb')

        with pytest.raises(ValueError):
            # Wrong input
            user_mapping = UserMapping(
                mapping_type='Wrong input',     # noqa
            )
            user_mapping.map('7c1cd6ae-8f35-4ce6-9631-d05901dc41bb')
