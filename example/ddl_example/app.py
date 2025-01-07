from flask import Flask
from dedi_link.model import DdlConfig

from ddl_example.models import BaseModel
from ddl_example.views import network_blueprint, user_blueprint


def create_app(database_file: str = None,
               ddl_config: DdlConfig = None,
               ):
    BaseModel.db.load_from_file(
        database_file=database_file,
    )

    app = Flask('Decentralised Discovery Link Example')

    if ddl_config is not None:
        app.config['DdlConfig'] = ddl_config
    else:
        app.config['DdlConfig'] = DdlConfig()

    app.register_blueprint(network_blueprint, url_prefix='/network')
    app.register_blueprint(user_blueprint, url_prefix='/user')

    return app


if __name__ == '__main__':
    app = create_app()

    # Run with debug setup
    app.run(
        host='127.0.0.1',
        port=5000,
    )
