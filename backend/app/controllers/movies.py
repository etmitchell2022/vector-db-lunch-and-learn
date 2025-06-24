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
            movies = [
                self.create_movie_obj(movie)
                for movie in movie_data
                if int(movie["id"]) == int(movie_id)
            ]
            return movies

    def get_movie_recommendations(self, search, top_n=5):
        embedding = self.embeddings.create_embedding(search)
        collection = self.db_client.get_or_create_collection("movies")

        results = collection.query(
            query_embeddings=[embedding],
            n_results=top_n,
            include=["metadatas", "distances"],
        )
        movies_with_scores = []
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        for metadata, distance in zip(metadatas, distances):
            metadata_with_score = metadata.copy()
            metadata_with_score["similarity"] = 1 - distance  # higher = more similar
            metadata_with_score["raw_similarity"] = distance
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
