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
        choices_data = [choice.to_dict() for choice in choices]
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
        if content is None or question_id is None:
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

# 선택지 상세 조회, 수정, 삭제
@choice_blp.route("/<int:choice_id>")
class ChoiceView(MethodView):
    # 선택지 상세 조회
    def get(self, choice_id):
        choice = app.models.Choice.query.get(choice_id)
        # 선택지가 존재하지 않으면 404 오류 반환
        if not choice:
            return jsonify({"message": "선택지를 찾을 수 없습니다."}), 404
        
        # 선택지 데이터 json 형식으로 반환
        return jsonify(choice.to_dict())
    
    def put(self, choice_id):
        # 선택지 조회
        choice = app.models.Choice.query.get(choice_id)
        # 선택지가 존재하지 않으면 404 오류 반환
        if not choice:
            return jsonify({"message": "선택지를 찾을 수 없습니다."}), 404
        
        # 요청 데이터 추출
        data = request.json
        # 선택지 수정
        try:
            # 요청 데이터에서 필드 추출
            choice.content = data.get("content", choice.content)
            choice.is_active = data.get("is_active", choice.is_active)
            choice.sqe = data.get("sqe", choice.sqe)
            choice.question_id = data.get("question_id", choice.question_id)
            
            # 커밋
            db.session.commit()
            # 성공 메세지 반환
            return jsonify({"message": "선택지가 성공적으로 수정되었습니다."})
        except Exception as e:
            # 예외 발생 시 롤백
            db.session.rollback()
            # 오류 메세지 반환
            return jsonify({"message": "선택지 수정 중 오류가 발생했습니다.", "error": str(e)}), 500
    
    # 선택지 삭제
    def delete(self, choice_id):
        # 선택지 조회
        choice = app.models.Choice.query.get(choice_id)
        # 선택지가 존재하지 않으면 404 오류 반환
        if not choice:
            return jsonify({"message": "선택지를 찾을 수 없습니다."}), 404
        
        # 선택지 삭제
        try:
            # 선택지 삭제
            db.session.delete(choice)
            # 커밋
            db.session.commit()
            # 성공 메세지 반환
            return jsonify({"message": "선택지가 성공적으로 삭제되었습니다."})
        except Exception as e:
            # 예외 발생 시 롤백
            db.session.rollback()
            # 오류 메세지 반환
            return jsonify({"message": "선택지 삭제 중 오류가 발생했습니다.", "error": str(e)}), 500