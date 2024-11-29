"""
Decentralised Discovery Link configuration object
"""

import importlib.resources as pkg_resources


class DDLConfig:
    """
    Configuration for a Decentralised Discovery Link node

    This configuration is used to initialise the service, and
    for it to know about itself and how to operate.
    """
    def __init__(self,
                 name: str = 'Decentralised Discovery Link',
                 description: str = 'A decentralised discovery service',
                 url: str = 'http://localhost:8000',
                 allow_non_client_authenticated: bool = False,
                 auto_user_registration: bool = False,
                 anonymous_access: bool = False,
                 default_ttl: int = 5,
                 optimal_record_percentage: float = 0.5,
                 time_score_weight: float = 0.5,
                 ema_factor: float = 0.5,
                 ):
        """
        Configuration for a Decentralised Discovery Link node

        This configuration is used to initialise the service, and for it to know
        about itself and how to operate.

        :param name: The name of the node
        :param description: A description of the node
        :param url: The URL of the node. This needs to be the URL where this node is
                    expected to be reached from other nodes
        :param allow_non_client_authenticated: Whether to allow requests with an access
                                               token that cannot be introspected
        :param auto_user_registration: Whether to automatically register users
        :param anonymous_access: Whether to allow anonymous access
        :param default_ttl: The default hops to relay a message
        :param optimal_record_percentage: The percentage of records to grant maximum score
        :param time_score_weight: The weight of time-based score in final score
        :param ema_factor: The factor for exponential moving average
        """
        self.name = name
        self.description = description
        self.url = url
        self.allow_non_client_authenticated = allow_non_client_authenticated
        self.auto_user_registration = auto_user_registration
        self.anonymous_access = anonymous_access
        self.default_ttl = default_ttl
        self.optimal_record_percentage = optimal_record_percentage
        self.time_score_weight = time_score_weight
        self.ema_factor = ema_factor

        self._bip_39 = None

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
