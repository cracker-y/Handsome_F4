from flask import request, jsonify
from flask_smorest import Blueprint
from flask.views import MethodView
from config import db
from models import Image


image_blp = Blueprint(
    "Images", __name__, description="Operations on images", url_prefix="/image"
)

# class Image(CommonModel):
#     __tablename__ = "images"
#     url = db.Column(db.TEXT, nullable=False)
#     type = db.Column(db.Enum(ImageStatus), nullable=False)

#     questions = db.relationship("Question", back_populates="image")

#     def to_dict(self):
#         return {
#             "id": self.id,
#             "url": self.url,
#             "type": self.type.value if hasattr(self.type, "value") else self.type,
#             "created_at": self.created_at.isoformat(),
#             "updated_at": self.updated_at.isoformat(),
#         }

@image_blp.route("/")
class ImageView(MethodView):
    def get(self):
        images = Image.query.all()
        images_data = [image.to_dict() for image in images]
        return jsonify(images_data)
    
    def post(self):
        data = request.json
        image = Image(url=data["url"], type=data["type"])
        db.session.add(image)
        db.session.commit()
        return jsonify({"message": "Image created successfully"})

