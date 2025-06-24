from flask.views import MethodView
from flask_smorest import Blueprint

ping_blp = Blueprint("Ping", "ping", description="Health check")


@ping_blp.route("/ping")
class PingResource(MethodView):
    @ping_blp.response(200)
    def get(self):
        return {"message": "pong"}
