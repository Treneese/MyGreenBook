# Standard library imports
from datetime import datetime
# Remote library imports
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

# Local imports
from config import db, bcrypt

# Association table for the many-to-many relationship between routes and places
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

    safety_marks = db.relationship('SafetyMark', backref='user', lazy=True)
    routes = db.relationship('Route', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

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
        self._password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User id={self.id} username={self.username} >'

class Place(db.Model, SerializerMixin):
    __tablename__ = 'places'

    serialize_rules = ('-reviews', '-safety_marks','-routes')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    safety_rating = db.Column(db.Float, nullable=False)

    reviews = db.relationship('Review', backref='place', lazy=True)
    safety_marks = db.relationship('SafetyMark', backref='place', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
    
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

    serialize_rules = ('-places', '-user')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    places = db.relationship('Place', secondary=route_place_association, backref=db.backref('routes', lazy='dynamic'))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'places': [place.to_dict() for place in self.places]
        }

    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) < 3:
            raise ValueError('Name must be at least 3 characters long')
        return name 

    def __repr__(self):
        return f'<Route id={self.id} name={self.name} user_id={self.user_id} place_id={self.place_id}>'

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    serialize_rules = ('-place.reviews')
# '-user.reviews'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user_name = db.Column(db.String(80), db.ForeignKey('users.name'), nullable=False)
    user_image = db.Column(db.String(500), db.ForeignKey('users.image'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utc, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'rating': self.rating,
            'place_id': self.place_id,
            'user_id': self.user_id,
            'user_name': self.user_name,
            'user_image': self.user_image,
            'created_at': self.created_at
        }
    
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

    serialize_rules = ('-place.safety_marks', '-user.safety_marks')

    id = db.Column(db.Integer, primary_key=True)
    is_safe = db.Column(db.Boolean, nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    @validates('is_safe')
    def validate_is_safe(self, key, is_safe):
        if not isinstance(is_safe, bool):
            raise ValueError('is_safe must be a boolean')
        return is_safe

    def __repr__(self):
        return f'<SafetyMark id={self.id} is_safe={self.is_safe} place_id={self.place_id} user_id={self.user_id}>'
