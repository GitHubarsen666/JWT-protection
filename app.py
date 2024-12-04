import os
from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from resources.auth import blp as AuthBlueprint
from db import db
from models.user import UserModel
from resources.cinema import blp as CinemaBlueprint
from resources.hall import blp as HallBlueprint
from resources.movie import blp as MovieBlueprint
from blocklist import BLOCKLIST

def create_app(db_url=None):
    app = Flask(__name__)
    
    # Конфігурація додатку
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Cinema API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = "jose"

    # Ініціалізація JWTManager
    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    # Ініціалізація бази даних
    db.init_app(app)
    
    # Ініціалізація API
    api = Api(app)

    # Створення контексту додатку перед викликом create_all
    with app.app_context():
        db.create_all()  # Створює таблиці, якщо вони ще не створені
        
        # Створення нового користувача, якщо його ще немає
        if not UserModel.query.filter_by(username='test_username').first():
            UserModel.create_user('test_username', 'test_password')
    
    # Реєстрація blueprints
    api.register_blueprint(CinemaBlueprint)
    api.register_blueprint(HallBlueprint)
    api.register_blueprint(MovieBlueprint)
    api.register_blueprint(AuthBlueprint)

    return app
