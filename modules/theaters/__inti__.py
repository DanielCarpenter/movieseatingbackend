from flask import Blueprint
from flask_restful import Api
from modules import app

theater_bp = Blueprint('theater_bp', __name__)
movies_api = Api(theater_bp)
app.register_blueprint(theater_bp)

from .models import *
from .routes import *
