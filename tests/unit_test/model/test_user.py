from uuid import uuid4, UUID
from pydantic import ValidationError
import pytest

from dedi_link.model.user import User


class TestUser:
    def test_init(self):
        user_id = uuid4()

        user = User(
            userId=user_id,
        )
        assert user.user_id == user_id

        user = User()
        assert isinstance(user.user_id, UUID)

    def test_model_validate(self):
        user_id = uuid4()
        user_dict = {
            'userId': str(user_id),
        }

        user = User.model_validate(user_dict)
        assert user.user_id == user_id

    def test_model_validate_error(self):
        user_dict = {
            'userId': 'invalid-uuid',
        }

        with pytest.raises(ValidationError):
            User.model_validate(user_dict)

    def test_model_dump(self):
        user_id = uuid4()

        user = User(
            userId=user_id,
        )

        user_dict = user.model_dump()
        assert user_dict == {
            'userId': str(user_id),
        }

    def test_model_dump_json(self):
        user_id = uuid4()

        user = User(
            userId=user_id,
        )

        user_json = user.model_dump_json()
        assert user_json == f'{{"userId":"{str(user_id)}"}}'
