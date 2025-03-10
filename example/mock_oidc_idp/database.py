import json
import os
import importlib.resources as pkg_resources
from threading import Lock


class InMemoryDatabase:
    def __init__(self):
        self.clients = {}
        self.users = {}
        self.tokens = {}

        self.commit_lock = Lock()

    def load_from_file(self):
        with pkg_resources.open_text(
            package='mock_oidc_idp.data',
            resource='mock_config.json'
        ) as f:
            data = json.load(f)

            self.clients = data['clients']
            self.users = data['users']
