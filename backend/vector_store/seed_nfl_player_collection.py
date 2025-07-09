import os
import json
import re
from embeddings import Embeddings
from chromadb_client import ChromaDBClient

POSITION_GROUPS = {
    "QB": "quarterback",
    "RB": "running_back",
    "FB": "running_back",
    "WR": "receiver",
    "TE": "receiver",
    "K": "kicker",
    "P": "punter",
    # Defensive positions
    "DE": "defensive",
    "DT": "defensive",
    "NT": "defensive",
    "OLB": "defensive",
    "ILB": "defensive",
    "MLB": "defensive",
    "LB": "defensive",
    "CB": "defensive",
    "S": "defensive",
    "SS": "defensive",
    "FS": "defensive",
    "DB": "defensive",
    # Offensive line
    "C": "offensive_line",
    "G": "offensive_line",
    "T": "offensive_line",
    "OL": "offensive_line",
}

STAT_CATEGORIES = {
    "quarterback": {
        "general": ["gamesPlayed", "fumbles", "fumblesLost"],
        "passing": [
            "completions",
            "passingAttempts",
            "passingYards",
            "passingTouchdowns",
            "interceptions",
            "yardsPerPassAttempt",
            "completionPct",
            "passingFirstDowns",
            "passingBigPlays",
            "longPassing",
            "sacks",
            "sackYardsLost",
            "QBRating",
        ],
        "rushing": [
            "rushingAttempts",
            "rushingYards",
            "rushingTouchdowns",
            "yardsPerRushAttempt",
        ],
    },
    "running_back": {
        "general": ["gamesPlayed", "fumbles", "fumblesLost"],
        "rushing": [
            "rushingAttempts",
            "rushingYards",
            "rushingTouchdowns",
            "yardsPerRushAttempt",
            "rushingFirstDowns",
            "rushingBigPlays",
            "longRushing",
            "stuffs",
        ],
        "receiving": [
            "receptions",
            "receivingYards",
            "receivingTouchdowns",
            "receivingTargets",
            "yardsPerReception",
            "receivingFirstDowns",
            "receivingYardsAfterCatch",
            "longReception",
        ],
    },
    "receiver": {
        "general": ["gamesPlayed", "fumbles", "fumblesLost"],
        "receiving": [
            "receptions",
            "receivingYards",
            "receivingTouchdowns",
            "receivingTargets",
            "yardsPerReception",
            "receivingFirstDowns",
            "receivingYardsAfterCatch",
            "longReception",
            "receivingBigPlays",
            "receivingFumbles",
            "netTotalYards",
            "netYardsPerGame",
        ],
        "rushing": [
            "rushingAttempts",
            "rushingYards",
            "rushingTouchdowns",
            "yardsPerRushAttempt",
        ],
    },
}


def seed_nfl_player_collection():
    raw_player_data = get_nfl_player_json()
    cleaned_player_data = [extract_player_data(player) for player in raw_player_data]

    vector_embeddings = create_player_embeddings(cleaned_player_data)

    db_client = ChromaDBClient()
    collection = db_client.get_or_create_collection("nfl_players")
    print("Inserting docs into collection", cleaned_player_data[0])
    # collection.add(
    #     documents=[create_player_description(player) for player in cleaned_player_data],
    #     embeddings=vector_embeddings,
    #     ids=[player["id"] for player in cleaned_player_data],
    #     metadatas=cleaned_player_data,
    # )
    print("Inserted docs:", len(collection.get()["documents"]))


def get_stat_value(player_data, category_name, stat_name):
    for category in player_data["raw_stats"]["splits"]["categories"]:
        if category["name"] == category_name:
            for stat in category["stats"]:
                if stat["name"] == stat_name:
                    return stat["value"]
    return 0.0


def extract_player_data(player_data):
    position = player_data.get("position").upper()
    position_group = POSITION_GROUPS.get(position, "general")

    player = {
        "name": player_data.get("name", ""),
        "position": position,
        "team": player_data.get("team", ""),
        "position_group": position_group,
        "id": player_data.get("espn_id", ""),
        "age": (
            int(player_data["age"]) if player_data.get("age") not in [None, ""] else ""
        ),
        "debut_year": (
            int(player_data["debutYear"])
            if player_data.get("debutYear") not in [None, ""]
            else ""
        ),
        "headshot": player_data.get("headshot", "") or "",
        "weight": (
            int(player_data["weight"])
            if player_data.get("weight") not in [None, ""]
            else ""
        ),
        "display_height": player_data.get("displayHeight", "") or "",
        "abbreviation": player_data.get("abbreviation", "") or "",
    }

    player_stat_categories = STAT_CATEGORIES.get(
        position_group, {"general": ["gamesPlayed"]}
    )
    for category, stats in player_stat_categories.items():
        print("category", category)
        for stat in stats:
            stat_key = to_snake_case(stat)
            player[stat_key] = get_stat_value(player_data, category, stat)
    return player


def get_position_specific_stats(player_data, position_filter):
    filtered_players = []
    for player in player_data:
        if player["position_group"].upper() == position_filter.upper():
            filtered_players.append(player)

    return filtered_players


def create_player_embeddings(player_data):
    embeddings_client = Embeddings()
    embeddings = []
    for player in player_data:
        print("Creating player description for", player["name"])
        input_text = create_player_description(player)
        vector = embeddings_client.create_embedding(input_text)
        embeddings.append(vector)

    return embeddings


def create_player_description(player_stats):
    position_group = player_stats["position_group"]

    if position_group == "quarterback":
        description = create_quarterback_description(player_stats)
    elif position_group == "running_back":
        description = create_running_back_description(player_stats)
    elif position_group == "receiver":
        description = create_receiver_description(player_stats)

    return description


def create_quarterback_description(player_stats):
    name = player_stats["name"]
    td_int_ratio = float(player_stats["passing_touchdowns"]) / max(
        1, float(player_stats["interceptions"])
    )
    total_tds = player_stats["passing_touchdowns"] + player_stats["rushing_touchdowns"]
    mobility_factor = float(player_stats["rushing_yards"]) / max(
        1, float(player_stats["games_played"])
    )

    # Determine QB archetype based on stats
    if mobility_factor > 30:
        if float(player_stats["yards_per_pass_attempt"]) > 7.5:
            archetype = "dual-threat playmaker"
        else:
            archetype = "mobile quarterback"
    elif float(player_stats["completion_pct"]) > 65:
        archetype = "accurate pocket passer"
    elif float(player_stats["yards_per_pass_attempt"]) > 8.0:
        archetype = "deep ball specialist"
    else:
        archetype = "game manager"

    description = f"""
    {name} is a {archetype} quarterback for the {player_stats['team']} with {player_stats["games_played"]} games of experience.
    
    Passing Profile: Completes {player_stats["completion_pct"]}% of passes ({player_stats["completions"]}/{player_stats["passing_attempts"]}) 
    for {player_stats["passing_yards"]} yards and {player_stats["passing_touchdowns"]} touchdowns against {player_stats["interceptions"]} interceptions.
    Efficiency metrics show {player_stats["yards_per_pass_attempt"]} yards per attempt with a {player_stats['q_b_rating']} passer rating.
    
    Decision Making: {td_int_ratio:.1f} touchdown-to-interception ratio demonstrates {'excellent' if td_int_ratio > 2.5 else 'good' if td_int_ratio > 1.5 else 'developing'} ball security.
    Generates {player_stats["passing_first_downs"]} first downs through the air with {player_stats["long_passing"]} completions of 20+ yards.
    
    Mobility Factor: Adds {player_stats["rushing_yards"]} rushing yards on {player_stats["rushing_attempts"]} attempts 
    ({player_stats["yards_per_rush_attempt"]} YPC) with {player_stats["rushing_touchdowns"]} rushing touchdowns.
    {'High mobility with' if mobility_factor > 30 else 'Moderate mobility with' if mobility_factor > 15 else 'Limited mobility with'} 
    {mobility_factor:.1f} rushing yards per game.
    
    Pressure Handling: Absorbed {player_stats["sacks"]} sacks for {player_stats["sack_yards_lost"]} yards lost, 
    showing {'good' if float(player_stats["sacks"]) / max(1, float(player_stats["games_played"])) < 2.5 else 'developing'} pocket presence.
    
    Overall Impact: {total_tds} total touchdowns across {player_stats["games_played"]} games as a 
    {'high-volume' if float(player_stats["passing_attempts"]) / max(1, float(player_stats["games_played"])) > 30 else 'moderate-volume'} passer.
    """

    return description.strip()


def create_running_back_description(player_stats):
    name = player_stats["name"]

    target_share = float(player_stats["receptions"]) / max(
        1, float(player_stats["receiving_targets"])
    )
    total_touches = float(player_stats["rushing_attempts"]) + float(
        player_stats["receptions"]
    )
    total_yards = float(player_stats["rushing_yards"]) + float(
        player_stats["receiving_yards"]
    )
    total_tds = float(player_stats["rushing_touchdowns"]) + float(
        player_stats["receiving_touchdowns"]
    )
    fumble_rate = float(player_stats["fumbles"]) / max(1, total_touches) * 100

    if float(player_stats["receiving_yards"]) > 400:
        if float(player_stats["rushing_attempts"]) > 200:
            archetype = "three-down workhorse back"
        else:
            archetype = "pass-catching specialist"
    elif float(player_stats["rushing_attempts"]) > 250:
        archetype = "power running back"
    elif float(player_stats["yards_per_rush_attempt"]) > 4.5:
        archetype = "explosive runner"
    else:
        archetype = "complementary back"

    description = f"""
    {name} is a {archetype} for the {player_stats['team']} with {player_stats["games_played"]} games of experience.
    
    Rushing Profile: Carries the ball {player_stats["rushing_attempts"]} times for {player_stats["rushing_yards"]} yards 
    ({player_stats["yards_per_rush_attempt"]} YPC) and {player_stats["rushing_touchdowns"]} touchdowns.
    Efficiency shows {'elite' if float(player_stats["yards_per_rush_attempt"]) > 4.5 else 'good' if float(player_stats["yards_per_rush_attempt"]) > 4.0 else 'average'} 
    yards per carry with {player_stats["rushing_first_downs"]} first downs and {player_stats["rushing_big_plays"]} explosive runs (20+ yards).
    
    Power Running: Longest rush of {player_stats["long_rushing"]} yards with {player_stats["stuffs"]} runs stuffed at or behind the line, 
    showing {'excellent' if float(player_stats["stuffs"]) / max(1, float(player_stats["rushing_attempts"])) < 0.08 else 'good' if float(player_stats["stuffs"]) / max(1, float(player_stats["rushing_attempts"])) < 0.12 else 'developing'} 
    ability to avoid negative plays.
    
    Receiving Ability: Catches {player_stats["receptions"]} passes on {player_stats["receiving_targets"]} targets 
    ({target_share:.1%} catch rate) for {player_stats["receiving_yards"]} yards and {player_stats["receiving_touchdowns"]} receiving touchdowns.
    Averages {player_stats["yards_per_reception"]} yards per catch with {player_stats["receiving_yards_after_catch"]} yards after catch, 
    demonstrating {'elite' if float(player_stats["receiving_yards"]) > 500 else 'good' if float(player_stats["receiving_yards"]) > 300 else 'limited'} pass-catching skills.
    
    Big Play Threat: Longest reception of {player_stats["long_reception"]} yards with {player_stats["receiving_first_downs"]} receiving first downs, 
    showing {'high' if float(player_stats["receiving_first_downs"]) > 20 else 'moderate' if float(player_stats["receiving_first_downs"]) > 10 else 'limited'} chain-moving ability through the air.
    
    Ball Security: {player_stats["fumbles"]} fumbles with {player_stats["fumbles_lost"]} lost on {total_touches:.0f} total touches 
    ({fumble_rate:.2f}% fumble rate), indicating {'excellent' if fumble_rate < 1.0 else 'good' if fumble_rate < 2.0 else 'concerning'} ball security.
    
    Overall Impact: {total_yards:.0f} total yards from scrimmage and {total_tds:.0f} total touchdowns as a 
    {'featured' if total_touches > 250 else 'rotational' if total_touches > 150 else 'situational'} back with 
    {'dual-threat' if float(player_stats["receiving_yards"]) > 300 else 'ground-focused'} versatility.
    """

    return description.strip()


def create_receiver_description(player_stats):
    name = player_stats["name"]

    # Calculate key metrics
    catch_rate = float(player_stats["receptions"]) / max(
        1, float(player_stats["receiving_targets"])
    )
    targets_per_game = float(player_stats["receiving_targets"]) / max(
        1, float(player_stats["games_played"])
    )
    yac_per_catch = float(player_stats["receiving_yards_after_catch"]) / max(
        1, float(player_stats["receptions"])
    )
    total_fumbles = float(player_stats["fumbles"]) + float(
        player_stats["receiving_fumbles"]
    )
    fumble_rate = total_fumbles / max(1, float(player_stats["receptions"])) * 100

    # Determine receiver archetype
    if float(player_stats["yards_per_reception"]) > 15:
        if float(player_stats["receiving_big_plays"]) > 15:
            archetype = "deep threat receiver"
        else:
            archetype = "vertical route specialist"
    elif targets_per_game > 8:
        if yac_per_catch > 6:
            archetype = "possession receiver with YAC ability"
        else:
            archetype = "high-volume possession receiver"
    elif float(player_stats["rushing_attempts"]) > 10:
        archetype = "versatile offensive weapon"
    elif yac_per_catch > 8:
        archetype = "yards-after-catch specialist"
    else:
        archetype = "reliable target"

    description = f"""
    {name} is a {archetype} for the {player_stats['team']} with {player_stats["games_played"]} games of experience.
    
    Receiving Production: Catches {player_stats["receptions"]} passes on {player_stats["receiving_targets"]} targets 
    ({catch_rate:.1%} catch rate) for {player_stats["receiving_yards"]} yards and {player_stats["receiving_touchdowns"]} touchdowns.
    Averages {player_stats["yards_per_reception"]} yards per reception with {targets_per_game:.1f} targets per game, 
    showing {'elite' if targets_per_game > 10 else 'high' if targets_per_game > 7 else 'moderate'} target share and usage.
    
    Route Running: Generates {player_stats["receiving_first_downs"]} first downs through the air with {player_stats["receiving_big_plays"]} explosive plays (20+ yards).
    Longest reception of {player_stats["long_reception"]} yards demonstrates {'elite' if float(player_stats["long_reception"]) > 60 else 'good' if float(player_stats["long_reception"]) > 40 else 'limited'} 
    big-play capability and {'excellent' if catch_rate > 0.70 else 'good' if catch_rate > 0.60 else 'developing'} hands.
    
    Yards After Catch: Accumulates {player_stats["receiving_yards_after_catch"]} YAC yards ({yac_per_catch:.1f} per catch), 
    indicating {'elite' if yac_per_catch > 7 else 'good' if yac_per_catch > 5 else 'limited'} ability to create after the catch.
    {'High YAC production shows' if yac_per_catch > 6 else 'Moderate YAC ability indicates'} 
    {'excellent' if yac_per_catch > 7 else 'solid' if yac_per_catch > 5 else 'developing'} elusiveness and run-after-catch skills.
    
    Versatility: Adds {player_stats["rushing_yards"]} rushing yards on {player_stats["rushing_attempts"]} carries 
    ({player_stats["yards_per_rush_attempt"]} YPC) with {player_stats["rushing_touchdowns"]} rushing touchdowns, 
    showing {'high' if float(player_stats["rushing_attempts"]) > 15 else 'moderate' if float(player_stats["rushing_attempts"]) > 5 else 'limited'} 
    offensive versatility beyond receiving.
    
    Ball Security: {total_fumbles:.0f} total fumbles ({player_stats["fumbles"]} general, {player_stats["receiving_fumbles"]} receiving) 
    with {player_stats["fumbles_lost"]} lost, resulting in {fumble_rate:.2f}% fumble rate per reception showing 
    {'excellent' if fumble_rate < 1.0 else 'good' if fumble_rate < 2.0 else 'concerning'} ball security.
    
    Overall Impact: {player_stats["net_total_yards"]} net total yards ({player_stats["net_yards_per_game"]} per game) as a 
    {'featured' if targets_per_game > 8 else 'complementary' if targets_per_game > 5 else 'rotational'} receiver with 
    {'elite' if float(player_stats["receiving_big_plays"]) > 12 else 'good' if float(player_stats["receiving_big_plays"]) > 6 else 'limited'} explosive play production.
    """

    return description.strip()


def get_nfl_player_json():
    base_dir = os.path.dirname(__file__)
    json_path = os.path.join(base_dir, "../data/nfl/nfl_data.json")
    with open(json_path) as f:
        nfl_data = json.load(f)
    return nfl_data


def to_snake_case(text):
    # Replace any existing hyphens or spaces with underscores and convert to lowercase
    text = re.sub(r"[\s-]", "_", text)
    # Insert an underscore before any uppercase letter that is not at the beginning of a word
    text = re.sub(r"(?<!^)([A-Z])", r"_\1", text)
    # Convert the entire string to lowercase
    return text.lower()


if __name__ == "__main__":
    seed_nfl_player_collection()
