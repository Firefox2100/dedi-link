from dedi_link.etc.exceptions import UserNotFound
from dedi_link.model import User as UserLib

from .base_model import BaseModel


class User(UserLib, BaseModel):
    @property
    def public_key(self) -> str:
        return self.db.user_keys['self'][self.user_id]['publicKey']

    @property
    def private_key(self) -> str:
        return self.db.user_keys['self'][self.user_id]['privateKey']

    @classmethod
    def load(cls, user_id: str) -> 'User':
        user_ids = cls.db.user_keys['self'].keys()

        if user_id not in user_ids:
            raise UserNotFound(user_id)

        return cls(
            user_id=user_id,
        )

    @classmethod
    def load_all(cls) -> list['User']:
        user_ids = cls.db.user_keys['self'].keys()

        users = []

        for user_id in user_ids:
            users.append(cls(
                user_id=user_id,
            ))

        return users
