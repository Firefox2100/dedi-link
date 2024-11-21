import pytest
from deepdiff import DeepDiff

from dedi_link.etc.exceptions import UserNotImplemented
from dedi_link.model import User


@pytest.fixture
def mock_user_1():
    return User(
        user_id='19a80cb0-7861-42c9-9212-c2e0cbe8dcfb',
    )


@pytest.fixture
def mock_user_dict_1():
    return {
        'userId': '19a80cb0-7861-42c9-9212-c2e0cbe8dcfb',
    }


@pytest.fixture
def mock_user_2():
    return User(
        user_id='c762a2e0-d7c1-4949-80a6-53e217371de0',
    )


class TestUser:
    def test_init(self):
        user = User(
            user_id='19a80cb0-7861-42c9-9212-c2e0cbe8dcfb',
        )

        assert user.user_id == '19a80cb0-7861-42c9-9212-c2e0cbe8dcfb'

    def test_equality(self, mock_user_1, mock_user_2):
        assert mock_user_1 == User(
            user_id='19a80cb0-7861-42c9-9212-c2e0cbe8dcfb',
        )

        assert mock_user_1 != mock_user_2

        assert mock_user_1 != 'Random String'

    def test_hash(self, mock_user_1):
        user_hash = hash(mock_user_1)

        assert isinstance(user_hash, int)

    def test_to_dict(self, mock_user_1, mock_user_dict_1):
        assert not DeepDiff(
            mock_user_1.to_dict(),
            mock_user_dict_1,
            ignore_order=True,
        )

    def test_from_dict(self, mock_user_1, mock_user_dict_1):
        user = User.from_dict(mock_user_dict_1)

        assert user == mock_user_1

    def test_public_key(self, mock_user_1):
        with pytest.raises(UserNotImplemented):
            _ = mock_user_1.public_key

    def test_private_key(self, mock_user_1):
        with pytest.raises(UserNotImplemented):
            _ = mock_user_1.private_key
