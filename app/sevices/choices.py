from flask import request, jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from config import db
from models import Board


choice_blp = Blueprint(
    "Choices", __name__, description="Operations on choices", url_prefix="/choice"
)