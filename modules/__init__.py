from flask import render_template, Flask, Blueprint
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)

#provides the settings for the applications
import config

api = Api(app)
ma = Marshmallow(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)

movies_bp = Blueprint('movies_bp', __name__)
movies_api = Api(movies_bp)
app.register_blueprint(movies_bp)

account_bp = Blueprint('account_bp', __name__)
account_api = Api(account_bp)
app.register_blueprint(account_bp)

from modules.models.user_models import *
from modules.models.movie_models import *
from modules.models.theater_models import *

import modules.admin
from modules.controllers.user_controllers import *
from modules.controllers.movie_controllers import *
from modules.controllers.theater_controllers import *
from modules.controllers.showing_controllers import *



@app.route('/')
def index():
    return render_template('index.html')

movies_api.add_resource(OneMovie, '/movie')
movies_api.add_resource(MovieList, '/movie/all')

account_api.add_resource(ApiRegister, '/register')
account_api.add_resource(ApiLogin, '/login')
account_api.add_resource(TokenRefresh, '/refresh')
account_api.add_resource(ShowingList, '/showing/all')
account_api.add_resource(OneShowing, '/showing')
account_api.add_resource(Reservations, '/reserve')


db.create_all()