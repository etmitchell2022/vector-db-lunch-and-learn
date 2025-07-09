import requests
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(BASE_DIR, "movie_data.json")


def get_movie_data():
    MAX_PAGES = 10
    movie_list = []
    for page in range(1, MAX_PAGES + 1):
        print(f"Fetching page {page}")
        url = f"https://api.themoviedb.org/3/movie/popular?language=en-US&page={page}"

        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {os.getenv('TMDB_API_KEY')}",
        }

        response = requests.get(url, headers=headers)
        movie_list.extend(response.json())
    unique_movies = remove_duplicates(movie_list)
    return unique_movies


# URL for image https://image.tmdb.org/t/p/w185/<PATH_ID>


def remove_duplicates(movie_list):
    unique_movies = []
    for movie in movie_list:
        if movie["id"] not in [movie["id"] for movie in unique_movies]:
            unique_movies.append(movie)
    return unique_movies


movie_data = get_movie_data()
with open(output_path, "w") as f:
    json.dump(movie_data, f, ensure_ascii=False)
