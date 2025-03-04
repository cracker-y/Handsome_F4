from flask import request, jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from config import db
from models import Board


image_blp = Blueprint(
    "Images", __name__, description="Operations on images", url_prefix="/image"
)