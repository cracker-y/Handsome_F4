from flask import request, jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from config import db
import app.models


choice_blp = Blueprint(
    "Choices", __name__, description="Operations on choices", url_prefix="/choice"
)

@choice_blp.route("/")
class ChoiceList(MethodView):
    # 모든 선택지를 조회
    def get(self):
        # 데이터베이스에서 모든 선택지 조회
        choices = app.models.Choice.query.all()
        choices_data = [
            {
                "content": self.content,
                "is_active": self.is_active,
                "sqe": self.sqe,
                "question_id": self.question_id,
            }
            for choice in choices
        ]
        # 선택지 데이터 json 형식으로 반환
        return jsonify(choices_data)
    
    # 새로운 선택지 생성
    def post(self):
        # 요청 본문에서 json 데이터 추출
        data = request.json
        content = data.get("content")
        is_active = data.get("is_active")
        sqe = data.get("sqe")
        question_id = data.get("question_id")

        # 필수 필드 검증
        if not content or not question_id:
            return jsonify({"message": "content와 question_id가 필요합니다."}), 400
        
        # 새로운 choices 객체 생성
        choice = app.models.Choice(
            content=content,
            is_active=is_active,
            sqe=sqe,
            question_id=question_id,
        )
        # 데이터베이스에 객체 추가, 커밋
        db.session.add(choice)
        db.session.commit()
        
        # 성공 메세지 반환
        return jsonify({"message": "선택지가 성공적으로 생성되었습니다."}), 201