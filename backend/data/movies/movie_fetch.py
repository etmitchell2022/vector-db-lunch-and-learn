import requests
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(BASE_DIR, "movie_data.json")


def get_movie_data():
    url = "https://api.themoviedb.org/3/movie/popular?language=en-US&page=1"

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {os.getenv('TMDB_API_KEY')}",
    }

    response = requests.get(url, headers=headers)

    return response.json()


# URL for image https://image.tmdb.org/t/p/w185/<PATH_ID>


movie_data = get_movie_data()
with open(output_path, "w") as f:
    json.dump(movie_data, f, ensure_ascii=False)
