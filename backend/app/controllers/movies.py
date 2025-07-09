import os
import json
from vector_store.chromadb_client import ChromaDBClient
from vector_store.embeddings import Embeddings


class MovieController:
    def __init__(self):
        self.db_client = ChromaDBClient()
        self.embeddings = Embeddings()

    def get_all_movies(self):
        base_dir = os.path.dirname(__file__)
        json_path = os.path.join(base_dir, "../../data/movies/movie_data.json")
        with open(json_path) as f:
            movie_data = json.load(f)
            movies = [self.create_movie_obj(movie) for movie in movie_data]
            return movies

    def get_movie_by_id(self, movie_id):
        base_dir = os.path.dirname(__file__)
        json_path = os.path.join(base_dir, "../../data/movies/movie_data.json")
        with open(json_path) as f:
            movie_data = json.load(f)
            movie = next(
                (
                    self.create_movie_obj(m)
                    for m in movie_data
                    if int(m["id"]) == int(movie_id)
                ),
                None,
            )
            return movie

    def get_movie_recommendations(self, search, top_n=5):
        embedding = self.embeddings.create_embedding(search)
        collection = self.db_client.get_or_create_collection("movies")

        results = collection.query(
            query_embeddings=[embedding],
            n_results=top_n + 1,
            include=["metadatas", "distances"],
        )
        movies_with_scores = []
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for metadata, distance in zip(metadatas[1:], distances[1:]):
            metadata_with_score = metadata.copy()
            metadata_with_score["similarity"] = round(
                1 - distance, 3
            )  # higher = more similar
            metadata_with_score["raw_similarity"] = round(distance, 3)
            metadata_with_score["popularity"] = round(metadata["popularity"], 1)
            metadata_with_score["vote_average"] = round(metadata["vote_average"], 1)
            movies_with_scores.append(metadata_with_score)

        return movies_with_scores

    def create_movie_obj(self, movie_data):
        return {
            "id": movie_data["id"],
            "title": movie_data["title"],
            "overview": movie_data["overview"],
            "vote_average": movie_data["vote_average"],
            "vote_count": movie_data["vote_count"],
            "popularity": movie_data["popularity"],
            "language": movie_data["original_language"],
            "poster_path": f"https://image.tmdb.org/t/p/w185/{movie_data['poster_path']}",
        }
