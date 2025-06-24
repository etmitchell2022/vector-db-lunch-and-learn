from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint

from app.controllers.movies import MovieController
from app.schemas.movies import MovieSearchArgs, MovieSchema

movies_blp = Blueprint("Movies", "movies", description="Movie Endpoints")


@movies_blp.route("/movies")
class MovieResource(MethodView):
    @movies_blp.response(200, MovieSchema(many=True))
    def get(self):
        movie_controller = MovieController()
        all_movies = movie_controller.get_all_movies()
        return all_movies


@movies_blp.route("/movies/search")
class MovieRecommendationResource(MethodView):
    @movies_blp.arguments(MovieSearchArgs, location="json")
    @movies_blp.response(200, MovieSchema(many=True))
    def post(self, args):
        movie_controller = MovieController()
        search = args.get("search")
        recommendations = movie_controller.get_movie_recommendations(search)
        return recommendations


@movies_blp.route("/movies/movie/<movie_id>")
class MovieResource(MethodView):
    @movies_blp.response(200, MovieSchema(many=True))
    def get(self, movie_id):
        movie_controller = MovieController()
        movie = movie_controller.get_movie_by_id(movie_id)
        return movie
