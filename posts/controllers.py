from flask import Blueprint
from flask import request
from flask import abort
from flask import Response
from extensions import db
import json

from decorators import verify_token


post = Blueprint('post', __name__)


@post.route('/', methods=['POST', "GET"])
@verify_token(methods=['POST'])
def posts():
    if request.method == 'POST':
        data = request.get_json(force=True)
        db.create_post(data)
        return Response(status=204, mimetype='application/json')
    elif request.method == 'GET':
        lim = int(request.args.get('limit', 10))
        off = int(request.args.get('offset', 0))
        return Response(json.dumps(db.get_posts(lim, off)), status=200, mimetype='application/json')


@post.route('/<post_id>', methods=['GET', 'PUT'])
@verify_token(methods=['PUT'])
def get_post(post_id):
    if request.method == 'GET':
        return Response(json.dumps(db.get_post_by_id(post_id)), status=200, mimetype='application/json')
    elif request.method == 'PUT':
        data = request.get_json(force=True)
        db.update_post(post_id=post_id, data=data)
        return Response(status=204, mimetype='application/json')


@post.route('/delete/<post_id>', methods=['DELETE'])
@verify_token(methods=['DELETE'])
def delete_post(post_id):
    if request.method == 'DELETE':
        db.delete_post(post_id=post_id)
        return Response(status=204, mimetype='application/json')
    else:
        return abort(404)
