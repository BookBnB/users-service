from flask import jsonify
from flask import Blueprint
from project.db import db
from project.models.user import User

bp = Blueprint('v1', __name__, url_prefix='/v1')

@bp.route("/")
def hello_world():
	return jsonify(hello="world")

@bp.route("/users/<email>", methods=["POST"])
def user_create(email):
	u = User(email)
	db.session.add(u)
	db.session.commit()
	return jsonify(message="ok")

@bp.route("/users")
def users():
	users = User.query.all()
	return jsonify([u.serialize() for u in users])
