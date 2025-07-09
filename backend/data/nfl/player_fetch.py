import requests
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

output_path = os.path.join(BASE_DIR, "nfl_data.json")


def get_all_nfl_players_by_position(positions=["QB", "WR", "RB"]):
    players = get_team_rosters(positions)
    result = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_player = {executor.submit(fetch_player_stats, p): p for p in players}
        for future in as_completed(future_to_player):
            player_data = future.result()
            if player_data:
                result.append(player_data)

    return result


def get_team_rosters(positions=["QB", "WR", "RB"]):
    teams = requests.get(
        "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams"
    ).json()["sports"][0]["leagues"][0]["teams"]
    players = []

    for team in teams:
        team_id = team["team"]["id"]
        roster = requests.get(
            f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}?enable=roster"
        ).json()["team"]["athletes"]
        # print("roster", roster["team"]["athletes"])

        for player in roster:
            pos = player["position"]["abbreviation"]
            if pos in positions:
                players.append(
                    {
                        "weight": player.get("weight"),
                        "displayHeight": player.get("displayHeight", ""),
                        "name": player.get("fullName", ""),
                        "espn_id": player.get("id", ""),
                        "position": pos,
                        "team": team["team"].get("displayName", ""),
                        "age": player.get("age"),
                        "debutYear": player.get("debutYear"),
                        "headshot": player.get("headshot", {}).get("href", ""),
                        "abbreviation": team["team"].get("abbreviation", ""),
                    }
                )
    return players


def fetch_player_stats(player):
    try:
        print(player["name"])
        url = f"https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes/{player['espn_id']}/statistics"
        res = requests.get(url)
        if res.status_code != 200:
            print(f"Failed to fetch stats for {player['name']}")
            return None
        stats = res.json()
        return {**player, "raw_stats": stats}
    except Exception as e:
        print(f"Failed to fetch stats for {player['name']}: {e}")
        return None


players = get_all_nfl_players_by_position()
# print(players, "players retrieved")
with open(output_path, "w") as f:
    json.dump(players, f, ensure_ascii=False)
