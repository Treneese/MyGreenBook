# Standard library imports
from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.associationproxy import association_proxy
# Remote library imports
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates



# Local imports
from config import db, bcrypt

route_place_association = db.Table('route_place_association',
    db.Column('route_id', db.Integer, db.ForeignKey('routes.id'), primary_key=True),
    db.Column('place_id', db.Integer, db.ForeignKey('places.id'), primary_key=True)
)

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-created_at', '-updated_at', '-_password_hash', '-safety_marks.user', '-routes.user', '-reviews.user')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.String(500))
    image = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    safety_marks = db.relationship('SafetyMark', backref='user_safety', lazy=True)
    routes = db.relationship('Route', backref='user_route', lazy=True)
    reviews = db.relationship('Review', backref='user_review', lazy=True)


    @validates('username')
    def validate_username(self, key, username):
        if not username or len(username) < 3:
            raise ValueError('Username must be at least 3 characters long')
        return username

    @validates('email')
    def validate_email(self, key, email):
        if not email or '@' not in email:
            raise ValueError('Invalid email address')
        return email


    @property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        self._password_hash = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    def set_password(self, password):
        if isinstance(password, str):
            password = password.encode('utf-8')
        self.password_hash = hashpw(password, gensalt()).decode('utf-8')


    def check_password(self, password):
        return checkpw(password.encode('utf-8'), self._password_hash.encode('utf-8'))


    def __repr__(self):
        return f'<User id={self.id} username={self.username} email={self.email}>'

class Place(db.Model, SerializerMixin):
    __tablename__ = 'places'

    serialize_rules = ('-reviews.place', '-safety_marks.place', '-routes.place')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    safety_rating = db.Column(db.Float, nullable=False)

    reviews = db.relationship('Review', backref='place_review', lazy=True)
    safety_marks = db.relationship('SafetyMark', backref='place_safety', lazy=True)

    @validates('name', 'city', 'address')
    def validate_string_fields(self, key, value):
        if not value or len(value) < 3:
            raise ValueError(f'{key.capitalize()} must be at least 3 characters long')
        return value

    @validates('safety_rating')
    def validate_safety_rating(self, key, safety_rating):
        if safety_rating < 0 or safety_rating > 5:
            raise ValueError('Safety rating must be between 0 and 5')
        return safety_rating

    def __repr__(self):
        return f'<Place id={self.id} name={self.name} city={self.city}>'

class Route(db.Model, SerializerMixin):
    __tablename__ = 'routes'

    serialize_rules = ('-places', '-user_route')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    places = db.relationship('Place', secondary=route_place_association, backref=db.backref('routes', lazy='dynamic'))

    
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) < 3:
            raise ValueError('Name must be at least 3 characters long')
        return name 

    def __repr__(self):
        return f'<Route id={self.id} name={self.name} user_id={self.user_id}>'

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    serialize_rules = ('-place_review.reviews', '-user_review.reviews')

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # place = db.relationship("Place", back_populates="reviews")
    # user = db.relationship("User", back_populates="reviews")

    @validates('content')
    def validate_content(self, key, content):
        if not content or len(content) < 10:
            raise ValueError('Content must be at least 10 characters long')
        return content

    @validates('rating')
    def validate_rating(self, key, rating):
        if rating < 0 or rating > 5:
            raise ValueError('Rating must be between 0 and 5')
        return rating

    def __repr__(self):
        return f'<Review id={self.id} rating={self.rating} place_id={self.place_id} user_id={self.user_id}>'

class SafetyMark(db.Model, SerializerMixin):
    __tablename__ = 'safetymarks'

    serialize_rules = ('-place_safety.safety_marks', '-user_safety.safety_marks')

    id = db.Column(db.Integer, primary_key=True)
    is_safe = db.Column(db.Boolean, nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # place = db.relationship("Place", back_populates="safetymarks")
    # user = db.relationship("User", back_populates="safetymarks")

    @validates('is_safe')
    def validate_is_safe(self, key, is_safe):
        if not isinstance(is_safe, bool):
            raise ValueError('is_safe must be a boolean')
        return is_safe

    def __repr__(self):
        return f'<SafetyMark id={self.id} is_safe={self.is_safe} place_id={self.place_id} user_id={self.user_id}>'
