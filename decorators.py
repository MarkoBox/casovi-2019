from functools import wraps
from flask import request, abort, current_app, g
import jwt

from extensions import db
# from users.exceptions import UserForbidden, UserUnauthorized, UserException
# from users.models import User


def verify_token(allow_anon=False, roles_required=None, methods=None):
    def verify_decorator(f):
        @wraps(f)
        def verify(*args, **kwargs):
            if request.method in methods:
                token = request.headers.get('Authorization', None)

                if not token:
                    abort(401, 'Token missing')
                token_split = str(token).split(" ")
                if token_split[0] != "Bearer":
                    abort(401, 'Invalid token')
                token = token_split[1]
                try:
                    payload = jwt.decode(token, current_app.config.get('SECRET_KEY'))
                    g.user = db.get_user_by_id(payload['_id'])
                    if not g.user:
                        abort(401, 'Invalid user')

                    # if roles_required:
                    #    if g.user.role.id not in roles_required:
                    #        raise UserForbidden('Insufficient privileges')
                except jwt.ExpiredSignatureError:
                    abort(401, 'Session expired,')
                except jwt.InvalidTokenError:
                    abort(401, 'Invalid Token.')
    #            except Exception as e:
    #                abort(401, 'Session problem')
            return f(*args, **kwargs)

        return verify

    return verify_decorator(allow_anon) if callable(allow_anon) else verify_decorator


def transactional(include_get=False):
    def transactional_decorator(f):
        @wraps(f)
        def transaction(*args, **kwargs):
            try:
                result = f(*args, **kwargs)
                # After done with a call, try to commit
                if request.method in ('POST', 'PUT', 'DELETE') or (include_get is True and request.method == 'GET'):
                    try:
                        db.session.commit()
                    except Exception:
                        current_app.logger.exception('DB commit failed')
                        abort(500, 'Server error')
                return result
            except Exception:
                db.session.rollback()
                raise
        return transaction
    return transactional_decorator(include_get) if callable(include_get) else transactional_decorator
