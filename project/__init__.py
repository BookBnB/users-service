from flask import Flask
from flask_migrate import Migrate
from project.db import db
from project.v1 import bp as bp_v1

def create_app():
	app = Flask(__name__)
	app.config.from_object("project.config.Config")

	db.init_app(app)

	migrate = Migrate(app, db)

	app.register_blueprint(bp_v1)

	return app
