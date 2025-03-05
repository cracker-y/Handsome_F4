from flask import request, jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from config import db
import app.models


question_blp = Blueprint(
    "Questions", __name__, description="Operations on questions", url_prefix="/question"
)


@question_blp.route("/")
class QuestionView(MethodView):
    def get(self):
        questions = app.models.Question.query.all()
        questions_data = [question.to_dict() for question in questions]
        return jsonify(questions_data)

    def post(self):
        data = request.json
        question = app.models.Question(
            title=data["title"],
            is_active=data["is_active"],
            sqe=data["sqe"],
            image_id=data["image_id"],
        )
        db.session.add(question)
        db.session.commit()
        return jsonify({"message": "Question created successfully"})


@question_blp.route("/<int:question_id>")
class QuestionView(MethodView):
    def get(self, question_id):
        question = app.models.Question.query.get(question_id)
        return jsonify(question.to_dict())

    def put(self, question_id):
        data = request.json
        with db.session.begin():
            question = app.models.Question.query.get(question_id)
            question.title = data["title"]
            question.is_active = data["is_active"]

    def delete(self, question_id):
        with db.session.begin():
            question = app.models.Question.query.get(question_id)
            db.session.delete(question)
        return jsonify({"message": "Question deleted successfully"})
    