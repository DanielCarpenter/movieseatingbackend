from flask import render_template
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)

#provides the settings for the applications
import common.config

api = Api(app)
ma = Marshmallow(app)
db = SQLAlchemy(app)
jwt = JWTManager(app)

import modules.movies
import modules.admin
import modules.accounts
import modules.access

@app.route('/')
def index():
    return render_template('index.html')
