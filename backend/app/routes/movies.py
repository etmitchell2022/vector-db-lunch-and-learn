from flask import Blueprint, jsonify, request

movies_bp = Blueprint("movies", __name__, url_prefix="/movies")
