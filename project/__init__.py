from flask import Flask
from flask_migrate import Migrate
from project.db import db
from project.v1 import bp as bp_v1

def create_app(test_config = {}):
	app = Flask(__name__)
	app.config.from_object("project.config.Config")
	app.config['SECRET_KEY'] = ''

	if test_config is not None:
		app.config.update(test_config)

	db.init_app(app)

	migrate = Migrate(app, db)

	app.register_blueprint(bp_v1)

	return app
