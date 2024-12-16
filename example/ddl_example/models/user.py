from dedi_link.model import User as UserLib

from .base_model import BaseModel


class User(UserLib, BaseModel):
    @property
    def public_key(self) -> str:
        return self.db.user_keys['self'][self.user_id]['publicKey']

    @property
    def private_key(self) -> str:
        return self.db.user_keys['self'][self.user_id]['privateKey']
