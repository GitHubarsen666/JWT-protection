from flask.views import MethodView
from flask_smorest import Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask import abort
from db import db
from schemas import CinemaSchema, PlainCinemaSchema
from models import CinemaModel
from flask_jwt_extended import jwt_required

blp = Blueprint("Cinemas", "cinemas", description="Operations on cinemas")

@blp.route("/cinema/<int:cinema_id>")
class Cinema(MethodView):
    @jwt_required()
    @blp.response(200, CinemaSchema)
    def get(self, cinema_id):
        cinema = CinemaModel.query.get_or_404(cinema_id)
        return cinema
    
    @jwt_required()
    def delete(self, cinema_id):
        cinema = CinemaModel.query.get_or_404(cinema_id)
        db.session.delete(cinema)
        db.session.commit()
        return {"message": "Cinema deleted"}, 200

    @blp.arguments(PlainCinemaSchema)
    @blp.response(200, CinemaSchema)
    def put(self, cinema_data, cinema_id):
        cinema = CinemaModel.query.get(cinema_id)
        if cinema:
            cinema.name = cinema_data["name"]
            cinema.location = cinema_data["location"]
        else:
            cinema = CinemaModel(id=cinema_id, **cinema_data)

        db.session.add(cinema)
        db.session.commit()
        return cinema

@blp.route("/cinema")
class CinemaList(MethodView):
    @jwt_required()
    @blp.response(200, CinemaSchema(many=True))
    def get(self):
        return CinemaModel.query.all()
    
    @jwt_required()
    @blp.arguments(PlainCinemaSchema)
    @blp.response(201, CinemaSchema)
    def post(self, cinema_data):
        cinema = CinemaModel(**cinema_data)
        try:
            db.session.add(cinema)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A cinema with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the cinema.")
        return cinema

