from typing import TypeVar

from dedi_link.etc.exceptions import UserNotImplemented
from .base_model import AsyncDataInterface
from ..user import UserB


UserT = TypeVar('UserT', bound='User')


class User(UserB, AsyncDataInterface):
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
