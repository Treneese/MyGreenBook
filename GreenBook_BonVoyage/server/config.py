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
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['SECRET_KEY'] = 'your_secret_key'
app.json.compact = False
CORS(app)

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
# db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*")
api = Api(app)


# 1. instantiate Bcrypt for password hashing
bcrypt = Bcrypt(app)

db.init_app(app)