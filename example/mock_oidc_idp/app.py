from flask import Flask

from .views import bp


def create_app():
    app = Flask('Mock OIDC Provider')

    app.register_blueprint(bp)

    return app


if __name__ == '__main__':
    app = create_app()

    # Run with debug setup
    app.run(
        host='127.0.0.1',
        port=5556,
    )
