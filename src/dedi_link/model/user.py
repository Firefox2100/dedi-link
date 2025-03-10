"""
User model.
"""

from typing import TypeVar, Type

from dedi_link.etc.exceptions import UserNotImplemented
from .base_model import BaseModel, SyncDataInterface


UserBaseT = TypeVar('UserBaseT', bound='UserBase')
UserT = TypeVar('UserT', bound='User')


class UserBase(BaseModel):
    """
    The base model for a User
    """
    def __init__(self,
                 user_id: str,
                 ):
        """
        The basic user model that is used for authentication and authorisation only.

        In implementation of this library this likely will be extended to include more
        information about the user, like email, name, etc.

        :param user_id: The user ID.
        """
        self.user_id = user_id

    def __eq__(self, other):
        if not isinstance(other, User):
            return NotImplemented

        return all([
            self.user_id == other.user_id,
        ])

    def __hash__(self):
        return hash((self.user_id,))

    def to_dict(self) -> dict:
        return {
            'userId': self.user_id,
        }

    @classmethod
    def from_dict(cls: Type[UserBaseT], payload: dict) -> UserBaseT:
        return cls(
            user_id=payload['userId'],
        )


class User(UserBase, SyncDataInterface):
    """
    The basic user model that is used for authentication and authorisation only.

    In implementation of this library this likely will be extended to include more
    information about the user, like email, name, etc.
    """
    @property
    def public_key(self) -> str:
        """
        The public key of the user.

        A user has a public/private key pair in RSA4096 that is used to
        encrypt the messages that carries actual data.

        :return: The public key of the user.
        """
        raise UserNotImplemented('public_key property not implemented')

    @property
    def private_key(self) -> str:
        """
        The private key of the user.

        :return: The private key of the user.
        """
        raise UserNotImplemented('private_key property not implemented')

    @classmethod
    def get_user_from_identity(cls,
                               idp: str,
                               subject_id: str,
                               email: str,
                               ):
        """
        Get the user from the identity provider.

        :param idp: The identity provider (the "iss" claim in the token).
        :param subject_id: The subject ID (the "sub" claim in the token).
        :param email: The email of the user (the "email" claim in the token).
        """
        raise UserNotImplemented('get_user_from_identity method not implemented')
