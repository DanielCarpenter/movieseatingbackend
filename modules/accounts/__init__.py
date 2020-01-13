from flask import Blueprint
from flask_restful import Api
from modules import app, api

account_bp = Blueprint('account_bp', __name__)
account_api = Api(account_bp)
app.register_blueprint(account_bp)

from .models import *
from .routes import *
