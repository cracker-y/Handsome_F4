from app import create_app, routes, jsonify
from flask import request
import app.models
from config import db

application = create_app()

# 홈페이지 접속 확인
@application.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Success Connect"})

# 회원가입
@application.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    # 필수 필드 추출
    name = data.get("name")
    email = data.get("email")
    age = data.get("age")
    gender = data.get("gender")

    # 유효성 검사 (name, email, age, gender 필수)
    if not name or not email or age is None or not gender:
        return jsonify({"error": "필수 입력값이 누락되었습니다."}), 400

    # 이메일 중복 확인
    existing_user = app.models.User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "이미 존재하는 계정입니다."}), 409

    try:
        # 사용자 생성
        new_user = app.models.User(name=name, email=email, age=age, gender=gender)
        
        # 데이터베이스 저장
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": f"{name}님 회원가입을 축하합니다.",
            "user_id": new_user.id,
            "age": age
        }), 200
    except Exception as e:
        db.session.rollback()  # 오류 발생 시 롤백
        return jsonify({"error": "회원가입 중 오류가 발생했습니다.", "details": str(e)}), 500

# 이미지 조회
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