import hashlib
import datetime
import jwt
from flask import current_app
import json


def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def generate_token(user_id, expiration=None):
    expiration = expiration if expiration else 60
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration),
        'iat': datetime.datetime.utcnow(),
        '_id': user_id
    }
    return jwt.encode(
        payload,
        current_app.config.get('SECRET_KEY'),
        algorithm='HS256'
    ).decode("utf-8")


def status_ok(result=None, message=None):
    output = {'status': 'ok'}

    if result:
        output['result'] = result
    else:
        output['result'] = []

    if message:
        output['message'] = message[0]

    return json.dumps(output)


