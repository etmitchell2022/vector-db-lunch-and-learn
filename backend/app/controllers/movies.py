import os
import json
from vector_store.chromadb_client import ChromaDBClient
from vector_store.embeddings import Embeddings
import umap
import numpy as np


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
            include=["metadatas", "distances", "documents", "embeddings"],
        )
        movies_with_scores = []
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]
        documents = results["documents"][0]
        embeddings = results["embeddings"][0]

        for metadata, distance, document, emb in zip(metadatas[1:], distances[1:], documents[1:], embeddings[1:]):
            metadata_with_score = metadata.copy()
            metadata_with_score["similarity"] = round(
                1 - distance, 3
            )  # higher = more similar
            metadata_with_score["raw_similarity"] = round(distance, 3)
            metadata_with_score["popularity"] = round(metadata["popularity"], 1)
            metadata_with_score["vote_average"] = round(metadata["vote_average"], 1)
            metadata_with_score["document"] = document
            metadata_with_score["embedding"] = emb.tolist()
            movies_with_scores.append(metadata_with_score)

        return movies_with_scores

    def create_vector_space_visualization(self, movie_id):
        collection = self.db_client.get_or_create_collection("movies")

        # Get the specific movie's embedding
        results = collection.get(
            ids=[movie_id], include=["embeddings", "metadatas", "documents"]
        )
        if not results["embeddings"]:
            return []
        
        embedding = results["embeddings"][0]

        # Get similar movies for visualization
        similar_movies = collection.query(
            query_embeddings=[embedding],
            n_results=10,
            include=["embeddings", "metadatas", "documents", "distances"],
        )

        movies_with_scores = []
        embeddings_to_reduce = []

        metadatas = similar_movies["metadatas"][0]
        distances = similar_movies["distances"][0]
        documents = similar_movies["documents"][0]
        embeddings = similar_movies["embeddings"][0]

        for metadata, distance, document, emb in zip(
            metadatas, distances, documents, embeddings
        ):
            metadata_with_score = metadata.copy()
            metadata_with_score["similarity"] = round(1 - distance, 3)
            metadata_with_score["raw_similarity"] = round(distance, 3)
            metadata_with_score["document"] = document
            metadata_with_score["embedding"] = emb.tolist()
            metadata_with_score["popularity"] = round(metadata["popularity"], 1)
            metadata_with_score["vote_average"] = round(metadata["vote_average"], 1)
            movies_with_scores.append(metadata_with_score)
            embeddings_to_reduce.append(emb)

        # Convert embeddings to 2D coordinates for visualization
        two_d_embeddings = self.convert_embeddings_to_2d_coordinates(
            embeddings_to_reduce
        )

        for movie, coords in zip(movies_with_scores, two_d_embeddings):
            movie["coordinates"] = {
                "x": float(round(coords[0], 3)),
                "y": float(round(coords[1], 3)),
            }
        return movies_with_scores

    def convert_embeddings_to_2d_coordinates(self, embeddings):
        reducer = umap.UMAP(n_components=2, random_state=42)
        return reducer.fit_transform(np.array(embeddings))

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
