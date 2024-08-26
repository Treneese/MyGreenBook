# Standard library imports
from datetime import datetime
# Remote library imports
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy import Table, Column, Integer, String, Boolean, Float, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
# Local imports
from config import db, bcrypt

# Association table for the many-to-many relationship between routes and places
route_place_association = db.Table('route_place_association',
    db.Column('route_id', db.Integer, db.ForeignKey('routes.id'), primary_key=True),
    db.Column('place_id', db.Integer, db.ForeignKey('places.id'), primary_key=True)
)

conversation_user_association = db.Table('conversation_user_association',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('conversation_id', db.Integer, db.ForeignKey('conversation.id'), primary_key=True)
)


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-created_at', '-updated_at', '-_password_hash', '-safety_marks.user', '-routes.user', '-reviews', '-following.user', '-followers.user')

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.String(500), default='Hi, I am passionate about discovering hidden gems and sharing travel tips from my adventures around the world. Join me as I explore vibrant cities, serene landscapes, and everything in between, helping you make the most of your journeys.')
    image = db.Column(db.String(500), default='https://static.vecteezy.com/system/resources/previews/016/774/588/original/3d-user-icon-on-transparent-background-free-png.png')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    first_name = db.Column(db.String(500), default='John')
    last_name = db.Column(db.String(500), default='Doe')
    location = db.Column(db.String(500), default='Huston,TX')


    safety_marks = db.relationship('SafetyMark', backref='user', lazy=True)
    routes = db.relationship('Route', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    followers = db.relationship('Follow', foreign_keys='Follow.following_id', backref='following_user', lazy='dynamic')
    following = db.relationship('Follow', foreign_keys='Follow.follower_id', backref='follower_user', lazy='dynamic', overlaps="follower_user,following")
   
    @validates('username')
    def validate_username(self, key, username):
        if not username or len(username) < 3:
            raise ValueError('Username must be at least 3 characters long')
        
        if self.query.filter_by(username=username).first():
            raise ValueError('Username is already taken')
        
        return username


    @validates('email')
    def validate_email(self, key, email):
        if not email or '@' not in email:
            raise ValueError('Invalid email address')
        
        if self.query.filter_by(email=email).first():
            raise ValueError('Email is already registered')

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
    safety_marks = db.relationship('SafetyMark', backref='place', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'address': self.address,
            'safety_rating': self.safety_rating
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

    serialize_rules = ('-place.reviews', '-user.reviews', '-comments.review', '-likes.review')

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(500))
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    likes = db.relationship('Like', backref='review', lazy=True,)
    comments = db.relationship('Comment', backref='review', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'rating': self.rating,
            'place_id': self.place_id,
            'image': self.image,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'likes': self.likes,
            'comments': [comment.to_dict() for comment in self.comments]

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
        return f'<Review id={self.id} rating={self.rating} place_id={self.place_id} user_id={self.user_id}  image={self.image} likes={self.likes} comments={self.comments}>'

class Like(db.Model, SerializerMixin):
    __tablename__ = 'likes'

    serialize_rules =()

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=False)
    liked_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


    def __repr__(self):
            return f'<Review id={self.id} user_id={self.user_id}>'

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


class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'

    serialize_rules = ('-review.comments', '-user.reviews')

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = relationship('User', backref='comments')

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'user_id': self.user_id,
            'review_id': self.review_id,
            'timestamp': self.timestamp
        }

def __repr__(self):
        return f'<Comment id={self.id} user_id={self.user_id}>'

class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    serialize_rules = ('-sender', '-conversation')

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    sender = relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    recipient = relationship('User', foreign_keys=[recipient_id], backref='received_messages')
    conversation = db.relationship('Conversation', backref='messages')

def __repr__(self):
        return f'<Message id={self.id} recipient_id={self.recipient_id} sender_id={self.sender_id}>'

class Conversation(db.Model, SerializerMixin):
    __tablename__ = 'conversation'

    serialize_rules = ('-user1', '-user2')

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sender = relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    recipient = relationship('User', foreign_keys=[recipient_id], backref='received_messages')

def __repr__(self):
       return f'<Conversation id={self.id} sender_id={self.sender_id} recipient_id={self.recipient_id}>'

class Notification(db.Model, SerializerMixin):
    __tablename__ = 'notifications'

    serialize_rules = ('-user')

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = relationship('User', backref='notifications')

def __repr__(self):
        return f'<Notification id={self.id} user_id={self.user_id} content={self.content[:20]}>'

class History(db.Model, SerializerMixin):
    __tablename__ = 'history'

    serialize_rules = ('-user')

    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = relationship('User', backref='history')

def __repr__(self):
        return f'<History id={self.id} user_id={self.user_id} action={self.action[:20]}>'

class Follow(db.Model, SerializerMixin):
    __tablename__ = 'follows'

    serialize_rules = ()
    
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    following_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())

    follower = relationship('User', foreign_keys=[follower_id], backref='following_relationships')
    following = relationship('User', foreign_keys=[following_id], backref='follower_relationships')

def __repr__(self):
      return f'<Follow id={self.id} follower_id={self.follower_id} following_id={self.following_id}>'

class Follower(db.Model, SerializerMixin):
    __tablename__ = 'followers'

    serialize_rules = ()

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = relationship('User', backref='followers')

def __repr__(self):
        return f'<Follower id={self.id} user_id={self.user_id}>'

class Following(db.Model, SerializerMixin):
    __tablename__ = 'followings'

    serialize_rules = ()

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = relationship('User', backref='followings')
    
def __repr__(self):
        return f'<Following id={self.id} user_id={self.user_id}>'

class Story(db.Model, SerializerMixin):
    __tablename__ = 'stories'

    serialize_rules = ()
    id = db.Column(db.Integer, primary_key=True)
    media = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = relationship('User', backref='stories')

    def to_dict(self):
        return {
            'id': self.id,
            'media': self.media,
            'user_id': self.user_id
        }
    
    def __repr__(self):
        return f'<Following id={self.id} media={self.media} user_id={self.user_id}>'

