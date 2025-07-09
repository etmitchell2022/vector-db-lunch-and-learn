import os
import json
import re
from vector_store.chromadb_client import ChromaDBClient
from vector_store.embeddings import Embeddings
from app.schemas.nfl_players import POSITION_GROUPS, STAT_CATEGORIES, ALL_STAT_KEYS
import umap
import numpy as np


class NFLPlayersController:
    def __init__(self):
        self.db_client = ChromaDBClient()
        self.embeddings = Embeddings()

    def get_all_players(self):
        base_dir = os.path.dirname(__file__)
        json_path = os.path.join(base_dir, "../../data/nfl/nfl_data.json")
        with open(json_path) as f:
            nfl_data = json.load(f)
            return self.create_player_object(nfl_data)

    def get_player_by_id(self, player_id):
        base_dir = os.path.dirname(__file__)
        json_path = os.path.join(base_dir, "../../data/nfl/nfl_data.json")
        with open(json_path) as f:
            nfl_data = json.load(f)
            player = next(
                (
                    self.extract_player_data(p)
                    for p in nfl_data
                    if int(p["espn_id"]) == int(player_id)
                ),
                None,
            )
            return player

    def get_similar_players(self, search, top_n=5):
        embedding = self.embeddings.create_embedding(search)
        collection = self.db_client.get_or_create_collection("nfl_players")

        results = collection.query(
            query_embeddings=[embedding],
            n_results=top_n,
            include=["metadatas", "distances", "documents", "embeddings"],
        )

        players_with_scores = []

        for metadata, distance, document, emb in zip(
            results["metadatas"][0],
            results["distances"][0],
            results["documents"][0],
            results["embeddings"][0],
        ):
            player = {
                "id": metadata.get("id", ""),
                "name": metadata.get("name", ""),
                "position": metadata.get("position", ""),
                "position_group": metadata.get("position_group", ""),
                "age": metadata.get("age") or 0,
                "debut_year": str(metadata.get("debut_year") or ""),
                "headshot": metadata.get("headshot") or "",
                "weight": float(metadata.get("weight") or 0.0),
                "display_height": metadata.get("display_height") or "",
                "team": metadata.get("team") or "",
                "abbreviation": metadata.get("abbreviation") or "",
                "embedding": emb.tolist(),
                "document": document,
                "similarity": round(1 - distance, 3),
                "raw_similarity": round(distance, 3),
                "stats": {},
            }
            for key in ALL_STAT_KEYS:
                player["stats"][key] = float(metadata.get(self.to_snake_case(key), 0.0))

            players_with_scores.append(player)

        return players_with_scores

    def create_vector_space_visualization(self, player_id):
        collection = self.db_client.get_or_create_collection("nfl_players")

        results = collection.get(
            ids=[player_id], include=["embeddings", "metadatas", "documents"]
        )
        embedding = results["embeddings"][0]

        similar_players = collection.query(
            query_embeddings=[embedding],
            n_results=10,
            include=["embeddings", "metadatas", "documents", "distances"],
        )

        players_with_scores = []
        embeddings_to_reduce = []

        metadatas = similar_players["metadatas"][0]
        distances = similar_players["distances"][0]
        documents = similar_players["documents"][0]
        embeddings = similar_players["embeddings"][0]

        for metadata, distance, document, emb in zip(
            metadatas, distances, documents, embeddings
        ):
            metadata_with_score = metadata.copy()
            metadata_with_score["similarity"] = round(1 - distance, 3)
            metadata_with_score["raw_similarity"] = round(distance, 3)
            metadata_with_score["document"] = document
            metadata_with_score["embedding"] = emb.tolist()
            players_with_scores.append(metadata_with_score)
            embeddings_to_reduce.append(emb)

        two_d_embeddings = self.convert_embeddings_to_2d_coordinates(
            embeddings_to_reduce
        )

        for player, coords in zip(players_with_scores, two_d_embeddings):
            player["coordinates"] = {
                "x": float(round(coords[0], 3)),
                "y": float(round(coords[1], 3)),
            }
        return players_with_scores

    def convert_embeddings_to_2d_coordinates(self, embeddings):
        reducer = umap.UMAP(n_components=2, random_state=42)
        return reducer.fit_transform(np.array(embeddings))

    def create_player_object(self, player_data):
        return [self.extract_player_data(player) for player in player_data]

    def get_stat_value(self, player_data, category_name, stat_name):
        for category in player_data["raw_stats"]["splits"]["categories"]:
            if category["name"] == category_name:
                for stat in category["stats"]:
                    if stat["name"] == stat_name:
                        return stat["value"]
        return 0.0

    def extract_player_data(self, player_data):
        position = player_data.get("position", "").upper()
        position_group = POSITION_GROUPS.get(position, "general")
        player = {
            "id": (
                player_data["espn_id"]
                if player_data.get("espn_id")
                else player_data["id"]
            ),
            "name": player_data["name"],
            "team": player_data.get("team"),
            "position": position,
            "position_group": position_group,
            "age": player_data.get("age"),
            "debut_year": player_data.get("debutYear"),
            "headshot": player_data.get("headshot"),
            "weight": player_data.get("weight"),
            "display_height": player_data.get("displayHeight"),
            "stats": {},
        }

        for stat in ALL_STAT_KEYS:
            player["stats"][stat] = 0.0

        stat_categories = STAT_CATEGORIES.get(position_group, {})
        for category, stats in stat_categories.items():
            for stat in stats:
                player["stats"][stat] = self.get_stat_value(player_data, category, stat)

        return player

    def to_snake_case(self, text):
        # Replace any existing hyphens or spaces with underscores and convert to lowercase
        text = re.sub(r"[\s-]", "_", text)
        # Insert an underscore before any uppercase letter that is not at the beginning of a word
        text = re.sub(r"(?<!^)([A-Z])", r"_\1", text)
        # Convert the entire string to lowercase
        return text.lower()
