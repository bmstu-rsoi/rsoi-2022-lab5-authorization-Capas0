import os
from functools import wraps

import requests
from authlib.integrations.flask_client import OAuth
from authlib.jose import jwt, JoseError
from dotenv import load_dotenv
from flask import request, jsonify

from .base import app

load_dotenv('.env')

app.secret_key = os.getenv("APP_SECRET_KEY")
oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=os.getenv("AUTH0_CLIENT_ID"),
    client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{os.getenv("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)

jwks = requests.get('https://dev-p7whdgfr521w6rkw.us.auth0.com/.well-known/jwks.json').json()


def authorized(f):
    @wraps(f)
    def check_token(*args, **kwargs):
        try:
            token = request.headers['Authorization'].replace('Bearer ', '')
            claims = jwt.decode(token, key=jwks)
            claims.validate()
            return f(*args, **kwargs)
        except (KeyError, JoseError):
            return jsonify(message='Unauthorized'), 401

    return check_token
