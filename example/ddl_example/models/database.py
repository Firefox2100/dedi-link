import json
import os
import importlib.resources as pkg_resources
from threading import Lock


class InMemoryDatabase:
    def __init__(self):
        self.networks = []
        self.nodes = []
        self.user_keys = {}

        self.commit_lock = Lock()

    def load_from_file(self,
                       database_file: str = None,
                       ):
        if database_file is not None:
            file_name = database_file
        else:
            file_name = os.getenv('DATABASE_FILE', 'database.1.json')

        with pkg_resources.open_text(
            package='ddl_example.data.db',
            resource=file_name
        ) as f:
            data = json.load(f)

            self.networks = data['networks']
            self.nodes = data['nodes']
            self.user_keys = data['userKeys']
