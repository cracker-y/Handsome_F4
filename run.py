from app import create_app, routes, jsonify
from flask import request
import app.models
from app.models import User, Question, Choice, Image, Answer
from app import db

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
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "이미 존재하는 계정입니다."}), 409

    try:
        # 사용자 생성
        new_user = User(name=name, email=email, age=age, gender=gender)
        
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

# 질문 조회
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

# 질문 생성
@application.route('/question', methods=['POST'])
def create_question():
    data = request.get_json()

    # 필수 필드 추출
    title = data.get("title")
    is_active = data.get("is_active")
    sqe = data.get("sqe")
    image_id = data.get("image_id")

    # 유효성 검사 (title 필수)
    if not title:
        return jsonify({"error": "질문 제목이 누락되었습니다."}), 400
    
    if not is_active:
        return jsonify({"error": "질문 활성화 여부가 누락되었습니다."}), 400
    
    if not sqe:
        return jsonify({"error": "질문 순서가 누락되었습니다."}), 400
    
    if not image_id:
        return jsonify({"error": "이미지 ID가 누락되었습니다."}), 400

    try:
        # 질문 생성
        new_question = Question(title=title, is_active=is_active, sqe=sqe, image_id=image_id)
        
        # 데이터베이스 저장
        db.session.add(new_question)
        db.session.commit()

        return jsonify({
            "message": f"Title: {title} Success Create"
        }), 200
    except Exception as e:
        db.session.rollback()  # 오류 발생 시 롤백
        return jsonify({"error": "질문 생성 중 오류가 발생했습니다.", "details": str(e)}), 500

# 선택지 생성
@application.route('/choice', methods=['POST'])
def create_choice():
    data = request.get_json()

    # 필수 필드 추출
    content = data.get("content")
    question_id = data.get("question_id")
    is_active = data.get("is_active")
    sqe = data.get("sqe")
    print(content, question_id, is_active, sqe)

    # 유효성 검사 (content, question_id 필수)
    if not content or question_id is None:
        return jsonify({"error": "필수 입력값이 누락되었습니다."}), 400

    try:
        # 선택지 생성
        new_choice = Choice(content=content, question_id=question_id, is_active=is_active, sqe=sqe)
        
        # 데이터베이스 저장
        db.session.add(new_choice)
        db.session.commit()

        return jsonify({
            "message": f"Content: {content} Success Create"
        }), 200
    except Exception as e:
        db.session.rollback()  # 오류 발생 시 롤백
        return jsonify({"error": "선택지 생성 중 오류가 발생했습니다.", "details": str(e)}), 500
    
    
@application.route('/image', methods=['POST'])
def create_image():
    data = request.get_json()

    # 필수 필드 추출
    url = data.get("url")
    type = data.get("type")

    # 유효성 검사 (url, type 필수)
    if not url or not type:
        return jsonify({"error": "필수 입력값이 누락되었습니다."}), 400
    
    try:
        # 이미지 생성
        new_image = Image(url=url, type=type)

        # 데이터베이스 저장
        db.session.add(new_image)
        db.session.commit()

        return jsonify({
            "message": f"Image: {url} Success Create"
        }), 200
    except Exception as e:
        db.session.rollback()  # 오류 발생 시 롤백
        return jsonify({"error": "이미지 생성 중 오류가 발생했습니다.", "details": str(e)}), 500



if __name__ == "__main__":
    application.run(debug=True)