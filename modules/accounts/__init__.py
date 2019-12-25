from flask import Blueprint
from flask_restful import Api
from modules import app, api

register_bp = Blueprint('register_bp', __name__)
register_api = Api(register_bp)
app.register_blueprint(register_bp)

from .models import *
from .routes import *
