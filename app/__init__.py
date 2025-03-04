from flask import Flask, jsonify
from flask_migrate import Migrate

import app.models

# from app.routes import routes
from app.sevices import images, users, questions
from config import db
from flask_smorest import Api

migrate = Migrate()


def create_app():
    application = Flask(__name__)

    application.config.from_object("config.Config")
    application.secret_key = "oz_form_secret"

    db.init_app(application)

    migrate.init_app(application, db)

    # 400 에러 발생 시, JSON 형태로 응답 반환
    @application.errorhandler(400)
    def handle_bad_request(error):
        response = jsonify({"message": error.description})
        response.status_code = 400
        return response

    # blurprint 설정
    # OpenAPI 관련 설정
    application.config["API_TITLE"] = "My API"
    application.config["API_VERSION"] = "v1"
    application.config["OPENAPI_VERSION"] = "3.1.3"
    application.config["OPENAPI_URL_PREFIX"] = "/"
    application.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    application.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )

    # 블루프린트 등록
    # application.register_blueprint(routes)
    api = Api(application)
    api.register_blueprint(images.image_blp)
    api.register_blueprint(users.user_blp)
    api.register_blueprint(questions.question_blp)
    with application.app_context():
        db.create_all()

    return application
