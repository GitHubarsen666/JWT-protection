from flask_smorest import Blueprint
from flask.views import MethodView
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from flask import request, jsonify
from werkzeug.security import check_password_hash
from db import db
from models.user import UserModel
import datetime

blp = Blueprint("Auth", "auth", description="Authentication and Authorization")

@blp.route("/login")
class Login(MethodView):
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        
        # Перевірка користувача
        user = UserModel.query.filter_by(username=username).first()
        if not user or not user.check_password(password):
            return {"message": "Invalid credentials"}, 401

        # Генерація токена
        access_token = create_access_token(identity=user.id, expires_delta=datetime.timedelta(hours=1))
        return {"access_token": access_token}, 200
    
@blp.route("/logout")
class Logout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]  # Отримуємо JWT ID
        return jsonify({"message": "Successfully logged out"}), 200






