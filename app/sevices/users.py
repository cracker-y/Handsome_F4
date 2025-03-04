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
                "id": user.id,
                "name": user.name,
                "age": user.age,
                "gender": user.gender,
                "email": user.email,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
            }
            for user in users
        ]
        return jsonify(users_data)

    def post(self):
        data = request.json
        user = app.models.User(
            id=data["id"],
            name=data["name"],
            age=data["age"],
            gender=data["gender"],
            email=data["email"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User created successfully"})
