from config import config, SELECTED_CONFIG
from flask import Flask
from user.controllers import user
from extensions import db
from posts.controllers import post
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler
import logging
from flask_migrate import Migrate


def create_app():
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi']
        }
    })

    app = Flask(__name__)

    app.config.from_object(config[SELECTED_CONFIG])

    db.init_app(app)
    migrate = Migrate(app, db)

    # Register the blueprints
    app.register_blueprint(user, url_prefix=app.config['APPLICATION_ROOT'] + '/user')
    app.register_blueprint(post, url_prefix=app.config['APPLICATION_ROOT'] + '/posts')

    handler = RotatingFileHandler('info_log.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    return app
