from db import db

class MovieModel(db.Model):
    __tablename__ = "movies"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    genre = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  
    hall_id = db.Column(db.Integer, db.ForeignKey("halls.id"), nullable=False)
    hall = db.relationship("HallModel", back_populates="movies")