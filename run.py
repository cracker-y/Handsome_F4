from app import create_app, routes, jsonify
from flask import request
import app.models

application = create_app()


@application.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Success Connect"})


@application.route("/image/<string:type>", methods=["GET"])
def get_image(type):
    image = app.models.Image.query.filter_by(type=type).first()

    return jsonify({"image": image.to_dict()["url"]})


@application.route("/questions/<int:question_id>")
def get_question_id(question_id):
    question = app.models.Question.query.filter_by(id=question_id).first()
    if not question:
        return jsonify({"message": "Question not found"}), 404

    choices = app.models.Choice.query.filter_by(question_id=question_id).all()

    return jsonify(
        {
            "id": question.id,
            "title": question.title,
            "image": (
                question.image.url if question.image else None
            ),  # 이미지가 없는 경우 대비
            "choices": [
                {
                    "id": choice.id,
                    "content": choice.content,
                }
                for choice in choices
            ],
        }
    )


if __name__ == "__main__":
    application.run(debug=True)
