from db import db

class CinemaModel(db.Model):
    __tablename__ = "cinemas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    location = db.Column(db.String(120), nullable=False)
    halls = db.relationship(
        "HallModel",
        back_populates="cinema",
        lazy="dynamic",
        cascade="all, delete"
    )
