from flask import request, jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from config import db
from models import Board


user_blp = Blueprint(
    "Users", __name__, description="Operations on users", url_prefix="/user"
)

