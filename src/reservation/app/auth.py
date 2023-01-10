from functools import wraps

import requests
from authlib.jose import jwt, JoseError
from flask import request, jsonify

jwks = requests.get('https://dev-p7whdgfr521w6rkw.us.auth0.com/.well-known/jwks.json').json()


def authorized(username=False):
    def decorator(f):
        @wraps(f)
        def check_token(*args, **kwargs):
            try:
                token = request.headers['Authorization'].replace('Bearer ', '')
                claims = jwt.decode(token, key=jwks)
                claims.validate()
                if username:
                    kwargs['username'] = claims['nickname']
                return f(*args, **kwargs)
            except (KeyError, JoseError):
                return jsonify(message='Unauthorized'), 401

        return check_token
    return decorator
