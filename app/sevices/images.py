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
        with db.session.begin():
            image = app.models.Image(
                url=data["url"],
                type=data["type"],
            )
            db.session.add(image)
        return jsonify({"message": "Image created successfully"})


@image_blp.route("/<int:image_id>")
class ImageView(MethodView):
    def get(self, image_id):
        image = app.models.Image.query.get(image_id)
        if not image:
            return jsonify({"message": "Image not found"}), 404
        return jsonify(image.to_dict())

    def put(self, image_id):
        image = app.models.Image.query.get(image_id)
        if not image:
            return jsonify({"message": "Image not found"}), 404

        data = request.json
        image.url = data["url"]
        image.type = data["type"]
        db.session.commit()
        return jsonify({"message": "Image updated successfully"})

    def delete(self, image_id):
        image = app.models.Image.query.get(image_id)
        if not image:
            return jsonify({"message": "Image not found"}), 404

        db.session.delete(image)
        db.session.commit()
        return jsonify({"message": "Image deleted successfully"})
