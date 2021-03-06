import os
from logging.config import dictConfig
from time import strftime

import yaml
from flasgger import Swagger
from flask import Flask
from flask_injector import FlaskInjector
from flask_migrate import Migrate
from prometheus_flask_exporter import PrometheusMetrics

from project.db import db
from project.infra.google_oauth import OAuth
from project.infra.tokenizer import Tokenizer
from project.services.users_service import UserService
from project.v1 import bp as bp_v1


def get_schemas():
    """
    Devuelve los schemas definidos en los archivos de swagger. Esto es necesario
    porque flasgger no soporta completamente la especificación OpenApi 3 y se
    necesita dicha versión para mergearla con el core.
    """
    schemas = {}
    for (dirpath, dirnames, filenames) in os.walk('project/swagger'):
        for filePath in (os.path.join(dirpath, file) for file in filenames):
            with open(filePath) as file:
                file_content = file.read()
                comment_index = file_content.rfind('---')
                if comment_index > 0:
                    comment_index = comment_index + 3
                else:
                    comment_index = 0
                content = yaml.safe_load((file_content[comment_index:]))
                schemas.update(content.get('components', {}).get('schemas', {}))
    return schemas


def config_logging(app):
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


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object("project.config.Config")

    if test_config is not None:
        app.config.update(test_config)

    db.init_app(app)

    Migrate(app, db)

    app.register_blueprint(bp_v1)

    configure_swagger(app)

    configure_dependencies(app)

    metrics = PrometheusMetrics(app=app, path='/metrics')

    config_logging(app)

    return app


def configure_swagger(app):
    template = {
        "openapi": "3.0.3",
        "components": {
            "schemas": get_schemas(),
            "examples": {},
            "securitySchemes": {
                "token": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "Authorization"
                }
            }
        }
    }

    Swagger(app, template=template)


def configure_dependencies(app):
    def configure(binder):
        binder.bind(
            OAuth,
            to=OAuth(app.config['GOOGLE_CLIENT_ID']),
        )

        binder.bind(
            Tokenizer,
            to=Tokenizer(app.config['SECRET_KEY'])
        )

    FlaskInjector(app, modules=[configure])
