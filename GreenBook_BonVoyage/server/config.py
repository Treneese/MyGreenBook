# Standard library imports

# Remote library imports
from sqlalchemy import MetaData

# Remote library imports
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask import request, Flask, jsonify, render_template, make_response, session
from flask_restful import Resource, Api
from flask_migrate import Migrate
from flask_socketio import SocketIO, send
from flask_cors import CORS
from sqlalchemy import MetaData
# from flask_session import Session


# Secret key for session encryption

# Configure server-side session


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'your_secret_key'
# app.json.compact = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(metadata=metadata)
# db = SQLAlchemy(app)
migrate = Migrate(app, db)
# jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*")
api = Api(app)
# bcrypt.init_app(app)
# socketio.init_app(app)
# api.init_app(app)

# Session(app)
# 1. instantiate Bcrypt for password hashing


db.init_app(app)
CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)