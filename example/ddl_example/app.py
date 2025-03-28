from flask import Flask
from dedi_link.model import DdlConfig, OidcDriver, OidcRegistry

from ddl_example.models import BaseModel
from ddl_example.views import network_blueprint, user_blueprint, federation_blueprint


def create_app(database_file: str = None,
               ddl_config: DdlConfig = None,
               oidc_registry: OidcRegistry = None
               ):
    BaseModel.db.load_from_file(
        database_file=database_file,
    )

    app = Flask('Decentralised Discovery Link Example')

    if ddl_config is None:
        ddl_config = DdlConfig()
    if oidc_registry is None:
        oidc_driver = OidcDriver(
            driver_id='http://localhost:5556',
            client_id='node1',
            client_secret='node_secret_1',
            discovery_url='http://localhost:5556/.well-known/openid-configuration',
        )

        oidc_registry = OidcRegistry()
        oidc_registry.register_driver(oidc_driver)

    BaseModel.init_config(
        config=ddl_config,
        oidc=oidc_registry,
    )

    app.register_blueprint(network_blueprint, url_prefix='/network')
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(federation_blueprint, url_prefix='/federation')

    return app


if __name__ == '__main__':
    app = create_app()

    # Run with debug setup
    app.run(
        host='127.0.0.1',
        port=5000,
    )
