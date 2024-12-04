from db import db

class HallModel(db.Model):
    __tablename__ = "halls"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    cinema_id = db.Column(db.Integer, db.ForeignKey("cinemas.id"), nullable=False)  

    cinema = db.relationship("CinemaModel", back_populates="halls")
    movies = db.relationship(
        "MovieModel",
        back_populates="hall",
        lazy="dynamic",
        cascade="all, delete"
    )

