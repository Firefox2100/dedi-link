"""
Decentralised Discovery Link configuration object
"""

from dataclasses import dataclass, field
import importlib.resources as pkg_resources


@dataclass
class DdlConfig:
    """
    Configuration for a Decentralised Discovery Link node

    This configuration is used to initialise the service, and
    for it to know about itself and how to operate.
    """
    name: str = 'Decentralised Discovery Link'
    description: str = 'A decentralised discovery service'
    url: str = 'http://localhost:8000'
    client_id: str = 'dedi-link'
    allow_non_client_authenticated: bool = False
    auto_user_registration: bool = False
    anonymous_access: bool = False
    trusted_issuers: list[str] = field(default_factory=list)
    default_ttl: int = 3
    optimal_record_percentage: float = 0.5
    time_score_weight: float = 0.5
    ema_factor: float = 0.5
    _bip_39: list[str] = field(default=None, repr=False)

    @property
    def bip_39(self) -> list[str]:
        """
        BIP-0039 word list
        """
        if self._bip_39 is None:
            with pkg_resources.open_text('dedi_link.data.resources', 'BIP-39.txt') as f:
                words = f.readlines()

            self._bip_39 = words

        return self._bip_39
