from secrets import token_urlsafe
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, redirect, request

from mock_oidc_idp.database import InMemoryDatabase


bp = Blueprint('mock_oidc_idp', __name__)
db = InMemoryDatabase()
db.load_from_file()


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


@bp.route('/token', methods=['POST'])
def token_endpoint():
    grant_type = request.form['grant_type']
    client_id = request.form.get('client_id')
    client_secret = request.form.get('client_secret')

    if client_id is None or client_secret is None:
        return {
            'error': 'Missing client ID or client secret'
        }, 400

    if client_id not in db.clients.keys() or client_secret != db.clients[client_id]['secret']:
        return {
            'error': 'Invalid client ID or client secret'
        }, 403

    sub = None
    refresh_token = None
    access_token = None

    if grant_type == 'password':
        # Direct access grant
        username = request.form.get('username')
        password = request.form.get('password')

        if username is None or password is None:
            return {
                'error': 'Username or password is missing'
            }, 400

        for user_id in db.users.keys():
            user = db.users[user_id]

            if username == user['username']:
                if user['password'] != password:
                    return {
                        'error': 'Invalid user credentials'
                    }, 403

                sub = user_id

        if sub is None:
            return {
                'error': 'User does not exist'
            }, 403
    elif grant_type == 'client_credentials':
        # Client credential grant
        sub = client_id
    elif grant_type == 'refresh_token':
        # Token refresh flow
        refresh_token = request.form.get('refresh_token')

        if refresh_token is None:
            return {
                'error': 'Refresh token missing'
            }, 400

        if refresh_token not in db.tokens.keys():
            return {
                'error': 'Invalid refresh token'
            }, 403

        token_data = db.tokens[refresh_token]

        if token_data['grant_time'] + timedelta(seconds=3600) < datetime.now():
            return {
                'error': 'Refresh token expired'
            }, 403

        if token_data['client_id'] != client_id:
            return {
                'error': 'Cannot refresh token issued for another client'
            }, 403

        access_token = token_urlsafe(32)
        token_data['access_token'] = access_token
        token_data['grant_time'] = datetime.now()
        sub = db.tokens[refresh_token]['sub']
    else:
        return {
            'error': 'Unsupported grant type'
        }, 400

    # Compose the token information
    if refresh_token is None:
        refresh_token = token_urlsafe(32)
        access_token = token_urlsafe(32)

        db.tokens[refresh_token] = {
            'access_token': access_token,
            'grant_time': datetime.now(),
            'sub': sub,
            'client_id': client_id,
        }

    return {
        'access_token': access_token,
        'refresh_token': refresh_token,
        'expires_in': 300,
        'token_type': 'bearer',
    }
