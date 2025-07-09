from flask import Flask
from flask_smorest import Api
from flask_cors import CORS
from app.routes.movies import movies_blp
from app.routes.ping import ping_blp
from app.routes.nfl_players import nfl_players_blp

URL_PREFIX = "/api/v1"


def create_app():
    app = Flask(__name__)

    CORS(app)

    app.config["API_TITLE"] = "Vector DB LnL demo API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/api/v1"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )

    api = Api(app)

    # Register Blueprints
    api.register_blueprint(ping_blp, url_prefix=URL_PREFIX)
    api.register_blueprint(movies_blp, url_prefix=URL_PREFIX)
    api.register_blueprint(nfl_players_blp, url_prefix=URL_PREFIX)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
