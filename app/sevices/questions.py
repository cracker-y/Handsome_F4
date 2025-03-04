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
        questions_data = [
            {
                "id": question.id,
                "title": question.title,
                "is_active": question.is_active,
                "sqe": question.sqe,
                "image": question.image.to_dict() if question.image else None,
                "created_at": question.created_at.isoformat(),
                "updated_at": question.updated_at.isoformat(),
            }
            for question in questions
        ]
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
