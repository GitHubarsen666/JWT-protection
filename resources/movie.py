from flask.views import MethodView
from flask_smorest import Blueprint
from flask import abort
from db import db
from models.movie import MovieModel
from schemas import MovieSchema, PlainMovieSchema

blp = Blueprint("Movies", "movies", description="Operations on movies")

@blp.route("/movie/<int:movie_id>")
class Movie(MethodView):
    @blp.response(200, MovieSchema)
    def get(self, movie_id):
        movie = MovieModel.query.get_or_404(movie_id)
        return movie

    def delete(self, movie_id):
        movie = MovieModel.query.get_or_404(movie_id)
        db.session.delete(movie)
        db.session.commit()
        return {"message": "Movie deleted"}, 200

    @blp.arguments(PlainMovieSchema)
    @blp.response(200, MovieSchema)
    def put(self, movie_data, movie_id):
        movie = MovieModel.query.get(movie_id)
        if movie:
            movie.title = movie_data["title"]
            movie.genre = movie_data["genre"]
            movie.duration = movie_data["duration"]
        else:
            movie = MovieModel(id=movie_id, **movie_data)

        db.session.add(movie)
        db.session.commit()
        return movie

@blp.route("/movie")
class MovieList(MethodView):
    @blp.response(200, MovieSchema(many=True))
    def get(self):
        return MovieModel.query.all()

    @blp.arguments(PlainMovieSchema)
    @blp.response(201, MovieSchema)
    def post(self, movie_data):
        movie = MovieModel(**movie_data)
        db.session.add(movie)
        db.session.commit()
        return movie
