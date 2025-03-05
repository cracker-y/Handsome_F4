from flask import request, jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from config import db
import app.models


answer_blp = Blueprint(
    "Answers", __name__, description="Operations on answers", url_prefix="/answer"
)


@answer_blp.route("/")
class AnswerList(MethodView):
    # 모든 답변 조회
    def get(self):
        # 데이터베이스에서 모든 답변 조회
        answers = app.models.Answer.query.all()
        # 답변 데이터를 json 형식으로 반환
        answers_data = [answer.to_dict() for answer in answers]
        # json 형식으로 반환
        return jsonify(answers_data)

    # 새로운 답변 생성
    def post(self):
        data = request.json
        user_id = data.get("user_id")
        choice_id = data.get("choice_id")

        # 필수 필드 검증
        if not user_id or not choice_id:
            return jsonify({"message": "user_id와 choice_id가 필요합니다."}), 400

        # 새로운 answers 객체 생성
        answer = app.models.Answer(
            user_id=user_id,
            choice_id=choice_id,
        )
        # 데이터베이스에 객체 추가, 커밋
        db.session.add(answer)
        db.session.commit()

        # 성공 메세지 반환
        return jsonify({"message": "답변이 성공적으로 생성되었습니다."}), 201
