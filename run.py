from app import create_app, routes, jsonify
from flask import request
import app.models
from config import db

application = create_app()


@application.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Success Connect"})


@application.route("/image/<string:type>", methods=["GET"])
def get_image(type):
    image = app.models.Image.query.filter_by(type=type).first()

    return jsonify({"image": image.to_dict()["url"]})


@application.route("/questions/<int:question_id>", methods=["GET"])
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
                    f"옵션 {choice.sqe}": choice.content,
                }
                for choice in choices
            ],
        }
    )


@application.route("/questions/count", methods=["GET"])
def get_question_count():
    question_count = app.models.Question.query.count()
    return jsonify({"total": question_count})


@application.route("/choice/<int:question_id>", methods=["GET"])
def get_choice(question_id):
    choices = app.models.Choice.query.filter_by(question_id=question_id).all()
    if not choices:
        return jsonify({"message": "Choice not found"}), 404

    return jsonify({"choices": [choice.to_dict() for choice in choices]})


@application.route("/submit", methods=["POST"])
def submit():
    datas = request.json
    user_id_list = []
    if not isinstance(datas, list):
        user_id = datas["user_id"]
        choice_id = datas["choice_id"]
        answers = app.models.Answer(user_id=user_id, choice_id=choice_id)
        db.session.add(answers)
        user_id_list.append(user_id)
    else:
        answers = []
        for data in datas:
            user_id = data["user_id"]
            choice_id = data["choice_id"]
            user_id_list.append(user_id)
            if not user_id or not choice_id:
                return (
                    jsonify({"message": "user_id와 choice_id가 필요합니다."}),
                    400,
                )
            answers.append(app.models.Answer(user_id=user_id, choice_id=choice_id))
        db.session.bulk_save_objects(answers)

    db.session.commit()
    return jsonify({"message": f"User: {user_id}'s answers Success Create"})


if __name__ == "__main__":
    application.run(debug=True)
