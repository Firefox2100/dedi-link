from secrets import token_urlsafe
from datetime import datetime, timedelta
from functools import wraps
from flask import Blueprint, request

from mock_oidc_idp.database import InMemoryDatabase


bp = Blueprint('mock_oidc_idp', __name__)
db = InMemoryDatabase()
db.load_from_file()


class OidcException(Exception):
    def __init__(self,
                 message: str,
                 status_code: int = 400,
                 ):
        self.message = message
        self.status_code = status_code


def exception_handler(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except OidcException as e:
            return {
                'error': e.message
            }, e.status_code
        except Exception as e:
            return {
                'error': 'Internal server error',
                'description': str(e)
            }, 500

    return wrapper


def authenticate_client(client_id: str, client_secret: str):
    if client_id is None or client_secret is None:
        raise OidcException('Missing client_id or client_secret')

    if client_id not in db.clients.keys() or client_secret != db.clients[client_id]['secret']:
        raise OidcException('Invalid client ID or client secret', 403)


def authenticate_user(username: str, password: str) -> str:
    sub = None

    if username is None or password is None:
        raise OidcException('Missing username or password')

    for user_id in db.users.keys():
        user = db.users[user_id]

        if username == user['username']:
            if user['password'] != password:
                raise OidcException('Invalid password', 401)

            sub = user_id

    if sub is None:
        raise OidcException('User does not exist', 403)

    return sub


def issue_token(sub: str, client_id: str) -> tuple[str, str]:
    refresh_token = token_urlsafe(32)
    access_token = token_urlsafe(32)

    db.tokens[refresh_token] = {
        'access_token': access_token,
        'grant_time': datetime.now(),
        'sub': sub,
        'client_id': client_id,
    }

    return access_token, refresh_token

@bp.route('/', methods=['GET'])
def index_endpoint():
    return "Success", 200


@bp.route('/.well-known/openid-configuration', methods=['GET'])
def openid_config_endpoint():
    return {
        'issuer': 'http://localhost:5556',
        'authorization_endpoint': 'http://localhost:5556/auth',
        'token_endpoint': 'http://localhost:5556/token',
        'introspection_endpoint': 'http://localhost:5556/introspect',
        'userinfo_endpoint': 'http://localhost:5556/userinfo',
    }


@exception_handler
@bp.route('/token', methods=['POST'])
def token_endpoint():
    grant_type = request.form['grant_type']
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')

    authenticate_client(
        client_id=client_id,
        client_secret=client_secret
    )

    refresh_token = None
    access_token = None

    if grant_type == 'password':
        # Direct access grant
        username = request.form.get('username')
        password = request.form.get('password')

        sub = authenticate_user(username, password)
    elif grant_type == 'client_credentials':
        # Client credential grant
        sub = client_id
    elif grant_type == 'refresh_token':
        # Token refresh flow
        refresh_token = request.form.get('refresh_token')

        if refresh_token is None:
            raise OidcException('Refresh token missing', 400)

        if refresh_token not in db.tokens.keys():
            raise OidcException('Invalid refresh token', 403)

        token_data = db.tokens[refresh_token]

        if token_data['grant_time'] + timedelta(seconds=3600) < datetime.now():
            raise OidcException('Refresh token expired', 403)

        if token_data['client_id'] != client_id:
            raise OidcException('Invalid client ID', 403)

        access_token = token_urlsafe(32)
        token_data['access_token'] = access_token
        token_data['grant_time'] = datetime.now()
        sub = db.tokens[refresh_token]['sub']
    else:
        raise OidcException('Invalid grant_type')

    # Compose the token information
    if refresh_token is None:
        access_token, refresh_token = issue_token(sub, client_id)

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'expires_in': 300,
        'token_type': 'bearer',
    }


@exception_handler
@bp.route('/introspect', methods=['POST'])
def introspect_endpoint():
    token = request.form['token']
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')

    if client_id is None and client_secret is None:
        # Could be using basic auth header
        client_id = request.authorization.get('username')
        client_secret = request.authorization.get('password')

    authenticate_client(
        client_id=client_id,
        client_secret=client_secret,
    )

    for refresh_token in db.tokens.keys():
        if db.tokens[refresh_token]['access_token'] == token:
            # Token is a match, check if it's expired
            if db.tokens[refresh_token]['grant_time'] + timedelta(seconds=300) < datetime.now():
                return {
                    'active': False
                }

            return {
                'active': True,
                'sub': db.tokens[refresh_token]['sub'],
                'client_id': db.tokens[refresh_token]['client_id'],
                'token_type': 'bearer',
                'scope': 'openid profile email',
                'exp': int((db.tokens[refresh_token]['grant_time'] + timedelta(seconds=300)).timestamp()),
                'iat': int(db.tokens[refresh_token]['grant_time'].timestamp()),
                'aud': [
                    client_id,
                ],
                'email': db.tokens[refresh_token]['sub'] if db.tokens[refresh_token]['sub'] != client_id else None,
                'username': db.users[db.tokens[refresh_token]['sub']]['username'],
            }

    raise OidcException('Invalid access token', 403)
