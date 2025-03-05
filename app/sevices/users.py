from flask import request, jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from config import db
import app.models


user_blp = Blueprint(
    "Users", __name__, description="Operations on users", url_prefix="/user"
)


@user_blp.route("/")
class UserView(MethodView):
    def get(self):
        users = app.models.User.query.all()
        # users_data = [
        #     {
        #         "id": user.id,
        #         "name": user.name,
        #         "age": user.age,
        #         "gender": user.gender,
        #         "email": user.email,
        #         "created_at": user.created_at,
        #         "updated_at": user.updated_at,
        #     }
        #     for user in users
        # ]
        users_data = [user.to_dict() for user in users]
        return jsonify(users_data)

    def post(self):
        data = request.json
        with db.session.begin():
            user = app.models.User(
                name=data["name"],
                age=data["age"],
                gender=data["gender"],
                email=data["email"],
            )
            db.session.add(user)
        return jsonify(
            {"message": "User님 회원가입을 축하합니다", "user_id": user.to_dict()["id"]}
        )


@user_blp.route("/<int:user_id>")
class UserView(MethodView):
    def get(self, user_id):
        user = app.models.User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404
        return jsonify(user.to_dict())

    def put(self, user_id):
        user = app.models.User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        data = request.json
        user.name = data["name"]
        user.age = data["age"]
        user.gender = data["gender"]
        user.email = data["email"]
        db.session.commit()
        return jsonify({"message": "User updated successfully"})

    def delete(self, user_id):
        user = app.models.User.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})
