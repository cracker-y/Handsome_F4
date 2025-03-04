from flask import request, jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from config import db
from models import Board


answer_blp = Blueprint(
    "Answers", __name__, description="Operations on answers", url_prefix="/answer"
)