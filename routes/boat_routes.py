from flask import Blueprint, request, jsonify
from app.database import get_db
from models.boat_model import add_boat

main = Blueprint('main', __name__)


