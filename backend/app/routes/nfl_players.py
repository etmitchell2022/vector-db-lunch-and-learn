from flask import jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from app.controllers.nfl_players import NFLPlayersController
from app.schemas.nfl_players import (
    NFLPlayerSchema,
    NFLPlayerSearchArgs,
    NFLPlayerSearchResultSchema,
    NFLPlayerVectorVisualizationSchema,
)

nfl_players_blp = Blueprint(
    "nfl_players", "nfl_Players", description="NFL Player stats endpoints"
)


@nfl_players_blp.route("/players")
class NFLPlayers(MethodView):
    @nfl_players_blp.response(200, NFLPlayerSchema(many=True))
    def get(self):
        nfl_players_controller = NFLPlayersController()
        all_players = nfl_players_controller.get_all_players()
        return all_players


@nfl_players_blp.route("/players/<player_id>")
class NFLPlayersById(MethodView):
    @nfl_players_blp.response(200, NFLPlayerSchema(many=False))
    def get(self, player_id):
        nfl_players_controller = NFLPlayersController()
        player = nfl_players_controller.get_player_by_id(player_id)
        return player


@nfl_players_blp.route("/players/similarity/search")
class NFLPlayersSimilaritySearch(MethodView):
    @nfl_players_blp.arguments(NFLPlayerSearchArgs, location="json")
    @nfl_players_blp.response(200, NFLPlayerSearchResultSchema(many=True))
    def post(self, args):
        search = args.get("search")
        nfl_players_controller = NFLPlayersController()
        similar_players = nfl_players_controller.get_similar_players(search)
        return similar_players


@nfl_players_blp.route("players/<player_id>/vector-visualization")
class NFLPlayersVectorSpaceVisualize(MethodView):
    @nfl_players_blp.response(200, NFLPlayerVectorVisualizationSchema(many=True))
    def get(self, player_id):
        nfl_players_controller = NFLPlayersController()
        players = nfl_players_controller.create_vector_space_visualization(player_id)
        return players
