from app import create_app, jsonify

app = create_app()


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Success Connect"})
