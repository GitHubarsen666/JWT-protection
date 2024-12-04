from flask.views import MethodView
from flask_smorest import Blueprint
from flask import abort
from db import db
from models.hall import HallModel
from schemas import HallSchema, PlainHallSchema

blp = Blueprint("Halls", "halls", description="Operations on halls")

# GET /hall/<int:hall_id> - отримання кінозалу за ID
@blp.route("/hall/<int:hall_id>")
class Hall(MethodView):
    @blp.response(200, HallSchema)
    def get(self, hall_id):
        hall = HallModel.query.get_or_404(hall_id)
        return hall

    # DELETE /hall/<int:hall_id> - видалення кінозалу за ID
    def delete(self, hall_id):
        hall = HallModel.query.get_or_404(hall_id)
        db.session.delete(hall)
        db.session.commit()
        return {"message": "Hall deleted"}, 200

    # PUT /hall/<int:hall_id> - оновлення кінозалу за ID
    @blp.arguments(PlainHallSchema)
    @blp.response(200, HallSchema)
    def put(self, hall_data, hall_id):
        hall = HallModel.query.get(hall_id)
        if hall:
            # Оновлюємо дані існуючого кінозалу
            hall.name = hall_data["name"]
            hall.capacity = hall_data["capacity"]
        else:
            # Якщо кінозал не знайдений, створюємо новий
            hall = HallModel(id=hall_id, **hall_data)

        db.session.add(hall)
        db.session.commit()
        return hall

@blp.route("/hall")
class HallList(MethodView):
    @blp.response(200, HallSchema(many=True))
    def get(self):
        return HallModel.query.all()

    @blp.arguments(PlainHallSchema)
    @blp.response(201, HallSchema)
    def post(self, hall_data):
        hall = HallModel(**hall_data)
        db.session.add(hall)
        db.session.commit()
        return hall