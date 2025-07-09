from marshmallow import Schema, fields

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

ALL_STAT_KEYS = sorted(
    set(
        stat
        for group in STAT_CATEGORIES.values()
        for cat in group.values()
        for stat in cat
    )
)


class StatsSchema(Schema):
    QBRating = fields.Float()
    completionPct = fields.Float()
    completions = fields.Float()
    fumbles = fields.Float()
    fumblesLost = fields.Float()
    gamesPlayed = fields.Float()
    interceptions = fields.Float()
    longPassing = fields.Float()
    longReception = fields.Float()
    longRushing = fields.Float()
    netTotalYards = fields.Float()
    netYardsPerGame = fields.Float()
    passingAttempts = fields.Float()
    passingBigPlays = fields.Float()
    passingFirstDowns = fields.Float()
    passingTouchdowns = fields.Float()
    passingYards = fields.Float()
    receivingBigPlays = fields.Float()
    receivingFirstDowns = fields.Float()
    receivingFumbles = fields.Float()
    receivingTargets = fields.Float()
    receivingTouchdowns = fields.Float()
    receivingYards = fields.Float()
    receivingYardsAfterCatch = fields.Float()
    receptions = fields.Float()
    rushingAttempts = fields.Float()
    rushingBigPlays = fields.Float()
    rushingFirstDowns = fields.Float()
    rushingTouchdowns = fields.Float()
    rushingYards = fields.Float()
    sackYardsLost = fields.Float()
    sacks = fields.Float()
    stuffs = fields.Float()
    yardsPerPassAttempt = fields.Float()
    yardsPerReception = fields.Float()
    yardsPerRushAttempt = fields.Float()


class NFLPlayerSchema(Schema):
    id = fields.Str(required=True)
    name = fields.Str(required=True)
    position = fields.Str(required=True)
    position_group = fields.Str(required=True)
    age = fields.Int()
    debut_year = fields.Str()
    headshot = fields.Str()
    weight = fields.Float()
    display_height = fields.Str()
    team = fields.Str()
    abbreviation = fields.Str()
    stats = fields.Nested(StatsSchema)


class NFLPlayerSearchArgs(Schema):
    search = fields.Str(required=True)


class NFLPlayerSearchResultSchema(NFLPlayerSchema):
    document = fields.Str()
    embedding = fields.List(fields.Float())
    similarity = fields.Float()
    raw_similarity = fields.Float()


class CoordinatesSchema(Schema):
    x = fields.Float()
    y = fields.Float()


class NFLPlayerVectorVisualizationSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    position = fields.Str()
    position_group = fields.Str()
    team = fields.Str()
    document = fields.Str()
    embedding = fields.List(fields.Float())
    similarity = fields.Float()
    raw_similarity = fields.Float()
    coordinates = fields.Nested(CoordinatesSchema)
