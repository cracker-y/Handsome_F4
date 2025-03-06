from app import create_app, jsonify
from flask.views import MethodView

app = create_app()


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Success Connect"})
