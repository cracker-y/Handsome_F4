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
                "url": image.url,
                "type": image.type,
            }
            for image in images
        ]
        return jsonify(images_data)

    def post(self):
        data = request.json
        image = app.models.Image(
            url=data["url"],
            type=data["type"],
        )
        db.session.add(image)
        db.session.commit()
        return jsonify({"message": "Image created successfully"})
