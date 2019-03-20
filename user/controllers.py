from flask import Blueprint
from flask import request
from flask import Response
from extensions import db
import json
import sqlite3
from utils import generate_token
import jwt
from flask import current_app, g
from user.model import User
from decorators import transactional

user = Blueprint('user', __name__)


@user.route('/register', methods=['POST'])
@transactional
def user_register():
    if request.method == 'POST':
        data = request.get_json(force=True)
        try:
            User.register(data)
        except sqlite3.IntegrityError:
            return Response(json.dumps({"message": "Username allready taken"}), status=400)
        return Response(status=204, mimetype='application/json')


@user.route('/login', methods=['POST'])
def user_login():
    if request.method == 'POST':
        data = request.get_json(force=True)
        try:
            user_object = db.get_user(data)
            response = {"token": generate_token(user_object[0]['id'])}
        except sqlite3.IntegrityError:
            return Response(json.dumps({"message": "Username allready taken"}), status=400)
        current_app.logger.info('%s logged in successfully', user_object[0]['username'])
        return Response(json.dumps(response), status=200, mimetype='application/json')


@user.route('/current_user', methods=['GET'])
def user_current():
    if request.method == 'GET':
        token = request.headers.get('Authorization', None)
        payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
        g.user = db.get_user_by_id(payload['_id'])
        return Response(json.dumps(g.user), status=200, mimetype='application/json')
