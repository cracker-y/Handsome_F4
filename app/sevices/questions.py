from flask import request, jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from config import db
from models import Board


question_blp = Blueprint(
    "Questions", __name__, description="Operations on questions", url_prefix="/question"
)