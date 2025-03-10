from typing import TypeVar

from dedi_link.etc.exceptions import UserNotImplemented
from .base_model import AsyncDataInterface
from ..user import UserBase


UserT = TypeVar('UserT', bound='User')


class User(UserBase, AsyncDataInterface):
    @property
    async def public_key(self) -> str:
        """
        The public key of the user.

        A user has a public/private key pair in RSA4096 that is used to
        encrypt the messages that carries actual data.

        :return: The public key of the user.
        """
        raise UserNotImplemented('public_key property not implemented')

    @property
    async def private_key(self) -> str:
        """
        The private key of the user.

        :return: The private key of the user.
        """
        raise UserNotImplemented('private_key property not implemented')

    @classmethod
    async def get_user_from_identity(cls,
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
