from flask import request, jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from config import db
import app.models


# def to_dict(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#             "age": self.age.value if hasattr(self.age, "value") else self.age,
#             "gender": (
#                 self.gender.value if hasattr(self.gender, "value") else self.gender
#             ),
#             "email": self.email,
#             "created_at": self.created_at.isoformat(),
#             "updated_at": self.updated_at.isoformat(),
#         }

user_blp = Blueprint(
    "Users", __name__, description="Operations on users", url_prefix="/user"
)


@user_blp.route("/")
class UserView(MethodView):
    def get(self):
        users = app.models.User.query.all()
        users_data = [
            {
                "name": user.name,
                "age": user.age,
                "gender": user.gender,
                "email": user.email,
            }
            for user in users
        ]
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
        return jsonify({"message": "User created successfully"})
