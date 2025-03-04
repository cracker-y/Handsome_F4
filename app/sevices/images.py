from flask import request, jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from config import db
import app.models


image_blp = Blueprint(
    "Images", __name__, description="Operations on images", url_prefix="/image"
)


@image_blp.route("/")
class ImageView(MethodView):
    def get(self):
        images = app.models.Image.query.all()
        images_data = [
            {
                "id": image.id,
                "url": image.url,
                "type": image.type,
                "created_at": image.created_at,
                "updated_at": image.updated_at,
            }
            for image in images
        ]
        return jsonify(images_data)

    def post(self):
        data = request.json
        image = app.models.Image(
            id=data["id"],
            url=data["url"],
            type=data["type"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )
        db.session.add(image)
        db.session.commit()
        return jsonify({"message": "Image created successfully"})
