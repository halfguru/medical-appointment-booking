"""
The flask connexion server configuration
"""
from connexion import App
from flask_cors import CORS, cross_origin
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import logging


logging.basicConfig(level=logging.INFO)

connexion_app = App(__name__)
app = connexion_app.app
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.sqlite3'

db = SQLAlchemy(app)
ma = Marshmallow(app)
