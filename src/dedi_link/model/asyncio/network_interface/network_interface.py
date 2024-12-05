import networkx as nx
from typing import TypeVar, Generic

from dedi_link.etc.exceptions import NetworkRequestFailed, NetworkInterfaceNotImplemented
from ...network_interface.network_interface import NetworkInterfaceB
from .session import Session, SessionT


class NetworkInterface(NetworkInterfaceB[SessionT],
                       Generic[SessionT],
                       ):
    SESSION_CLASS = Session

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    @property
    async def network_graph(self) -> nx.DiGraph:
        """
        Get a networkx.DiGraph representation of the network
        """
        raise NetworkInterfaceNotImplemented('network_graph method needs to be implemented by an application')

    async def close(self):
        await self.session.close()

    async def check_connectivity(self,
                                 url: str | None = None,
                                 path: str = '/api'
                                 ) -> bool:
        """
        Check whether the URL is reachable from the current machine.

        Note that this can only check the connectivity from the current machine.
        For example, the node may appear online, but it may be behind a firewall or filter
        that this machine can access while the others cannot

        If there is specific method to make it reachable (like a custom DNS record),
        it might still not be reachable from the outside, even if this method returns True.
        :param url: URL to check, None to check for the current node
        :param path: Path to check
        :return:
        """
        url = self._check_connectivity_url(
            url=url,
            path=path,
        )

        if url is None:
            return False

        try:
            async with self.SESSION_CLASS() as session:
                response = await session.get(url)
                return response['status'] == 'OK'
        except NetworkRequestFailed:
            return False

    async def find_path_to_node(self,
                          node_id: str,
                          ) -> list[list[str]]:
        """
        Tries to find the shortest path to a node in the network
        """
        async with self.network_graph as graph:
            return self._find_path_to_node(
                network_graph=graph,
                node_id=node_id,
            )
