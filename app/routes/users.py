from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash

auth_blp = Blueprint('auth', __name__)

@auth_blp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    # 인증 로직 구현
    return jsonify({"message": "Login successful"}), 200

@auth_blp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    # 회원가입 로직 구현
    return jsonify({"message": "Registration successful"}), 201