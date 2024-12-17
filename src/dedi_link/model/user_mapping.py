"""
User Mapping mechanism model

User mapping refers to the procedure of "virtually" changing the
user ID into a different one based on a set of rules. This is
used to accommodate different authentication system setup, where
one instance may not be able to correctly accept the credentials
from another one.
"""

from typing import TypeVar, Type
from deepdiff import DeepDiff

from dedi_link.etc.enums import MappingType
from .base_model import BaseModel


UserMappingT = TypeVar('UserMappingT', bound='UserMapping')


class UserMapping(BaseModel):
    """
    A class controlling how user IDs are mapped to other user IDs.

    User ID mapping is implemented in the case where incoming ID (for
    example, from a different IdP) does not correspond directly to the
    IDs used in this system, and mapping is required; or if there are
    special users like "anonymous" or "service" that are local accounts.
    """
    def __init__(self,
                 mapping_type: MappingType = MappingType.NO_MAPPING,
                 static_id: str = None,
                 dynamic_mapping: dict[str, str] = None,
                 ):
        """
        A class controlling how user IDs are mapped to other user IDs.

        User ID mapping is implemented in the case where incoming ID (for
        example, from a different IdP) does not correspond directly to the
        IDs used in this system, and mapping is required; or if there are
        special users like "anonymous" or "service" that are local accounts.

        :param mapping_type: The type of mapping to use
        :param static_id: The static ID to map to, if mapping type is static
        :param dynamic_mapping: The dynamic mapping to use, if mapping type is dynamic
        :raises ValueError: If the mapping type is static and no static ID is provided
        """
        self.mapping_type = mapping_type
        self.static_id = static_id
        self.dynamic_mapping = dynamic_mapping or {}

        if mapping_type == MappingType.STATIC and static_id is None:
            raise ValueError('Static ID is required for static mapping')

    def __eq__(self, other):
        if not isinstance(other, UserMapping):
            return NotImplemented

        if self.mapping_type != other.mapping_type:
            return False

        if self.mapping_type == MappingType.NO_MAPPING:
            return True
        elif self.mapping_type == MappingType.STATIC:
            return self.static_id == other.static_id
        elif self.mapping_type == MappingType.DYNAMIC:
            return not DeepDiff(
                self.dynamic_mapping,
                other.dynamic_mapping,
                ignore_order=True,
            )

        return False

    def to_dict(self) -> dict:
        payload = {
            'mappingType': self.mapping_type.value,
        }

        if self.mapping_type == MappingType.STATIC:
            payload['staticId'] = self.static_id
        elif self.mapping_type == MappingType.DYNAMIC:
            payload['dynamicMapping'] = self.dynamic_mapping

        return payload

    @classmethod
    def from_dict(cls: Type[UserMappingT], payload: dict) -> 'UserMapping':
        mapping_type = MappingType(payload.get('mappingType', MappingType.NO_MAPPING.value))
        static_id = payload.get('staticId')
        dynamic_mapping = payload.get('dynamicMapping')

        return UserMapping(
            mapping_type=mapping_type,
            static_id=static_id,
            dynamic_mapping=dynamic_mapping,
        )

    def dynamic_map(self,
                    user_id: str,
                    ) -> str:
        """
        Map a user ID to a new user ID using the dynamic mapping

        This method is extracted separately to allow easier override,
        in case some mapping systems use string manipulation instead
        of table lookup.

        :param user_id: The user ID to map
        :return: The mapped user ID
        :raises ValueError: If the user ID is not found in the mapping
        """
        new_id = self.dynamic_mapping.get(user_id)

        if new_id is None:
            raise ValueError(f'User ID {user_id} not found in mapping')

        return new_id

    def map(self,
            user_id: str | None = None,
            ) -> str:
        """
        Map a user ID to a new user ID based on the mapping type

        :param user_id: The user ID to map
        :return: The mapped user ID
        :raises ValueError: If the mapping type is invalid or no user ID is provided
        """
        if self.mapping_type == MappingType.NO_MAPPING:
            if user_id is None:
                raise ValueError('No user ID provided')
            return user_id

        if self.mapping_type == MappingType.STATIC:
            return self.static_id

        if self.mapping_type == MappingType.DYNAMIC:
            if user_id is None:
                raise ValueError('No user ID provided')
            return self.dynamic_map(user_id)

        raise ValueError(f'Invalid mapping type {self.mapping_type}')
