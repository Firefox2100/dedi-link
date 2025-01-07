import os

from dedi_link.model import DdlConfig
from ddl_example.app import create_app


def config_wrapper(node_id: str):
    if node_id == '1':
        app = create_app(
            database_file='database.1.json',
            ddl_config=DdlConfig(),
        )

        app.run(
            host='127.0.0.1',
            port=5000,
        )
    elif node_id == '2':
        app = create_app(
            database_file='database.2.json',
            ddl_config=DdlConfig(),
        )

        app.run(
            host='127.0.0.1',
            port=5001,
        )
    elif node_id == '3':
        app = create_app(
            database_file='database.3.json',
            ddl_config=DdlConfig(),
        )

        app.run(
            host='127.0.0.1',
            port=5002,
        )
    else:
        raise ValueError('Invalid node ID')


def main():
    node_id = os.getenv('DEMO_NODE_ID', '1')

    config_wrapper(node_id)


if __name__ == '__main__':
    main()
