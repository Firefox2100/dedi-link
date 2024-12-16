from flask import Flask

from ddl_example.models import BaseModel
from ddl_example.views import network_blueprint


def create_app():
    BaseModel.db.load_from_file()

    app = Flask('Decentralised Discovery Link Example')

    app.register_blueprint(network_blueprint, url_prefix='/network')

    return app


if __name__ == '__main__':
    app = create_app()

    # Run with debug setup
    app.run(
        host='127.0.0.1',
        port=5000,
        # debug=True,
    )
