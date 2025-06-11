import json
import os
from embeddings import Embeddings
from chromadb_client import ChromaDBClient


def seed_movie_collection():
    movie_data = get_movie_json()
    movies = [create_movie_obj(movie) for movie in movie_data["results"]]

    vector_embeddings = get_embeddings(movies)


def create_movie_obj(movie_data):
    return {
        "id": movie_data["id"],
        "title": movie_data["title"],
        "overview": movie_data["overview"],
        "vote_average": movie_data["vote_average"],
        "vote_count": movie_data["vote_count"],
        "popularity": movie_data["popularity"],
        "language": movie_data["original_language"],
        "poster_path": movie_data["poster_path"],
    }


def format_movie_for_embedding(movie):
    return (
        f"Title: {movie['title']}. "
        f"Overview: {movie['overview']}. "
        f"Language: {movie.get('language', 'unknown')}. "
        f"Average Rating: {movie['vote_average']}. "
        f"Vote Count: {movie['vote_count']}."
    )


def get_embeddings(movies):
    embeddings_client = Embeddings()
    embedded = []

    for movie in movies:
        input_text = format_movie_for_embedding(movie)
        print(f"Creating embedding for {movie['title']} with input: {input_text}")
        vector = embeddings_client.create_embedding(input_text)
        embedded.append((movie, vector))

    return embedded


def get_movie_json():
    base_dir = os.path.dirname(__file__)
    json_path = os.path.join(base_dir, "../data/movies/movie_data.json")
    with open(json_path) as f:
        movie_data = json.load(f)
    return movie_data


if __name__ == "__main__":
    seed_movie_collection()
