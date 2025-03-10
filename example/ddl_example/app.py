from flask import Flask
from dedi_link.model import DdlConfig, OidcDriver

from ddl_example.models import BaseModel
from ddl_example.views import network_blueprint, user_blueprint, federation_blueprint


def create_app(database_file: str = None,
               ddl_config: DdlConfig = None,
               oidc: OidcDriver = None
               ):
    BaseModel.db.load_from_file(
        database_file=database_file,
    )

    app = Flask('Decentralised Discovery Link Example')

    if ddl_config is None:
        ddl_config = DdlConfig()
    if oidc is None:
        oidc = OidcDriver(
            client_id='node1',
            client_secret='secret1',
            discovery_url='http://localhost:5556/.well-known/openid-configuration',
        )

    BaseModel.init_config(
        config=ddl_config,
        oidc=oidc,
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
