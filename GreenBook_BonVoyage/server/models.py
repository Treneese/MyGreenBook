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

#This File create the Instance of each Item.

# Association table for the many-to-many relationship between routes and places
route_place_association = db.Table('route_place_association',
    db.Column('route_id', db.Integer, db.ForeignKey('routes.id'), primary_key=True),
    db.Column('place_id', db.Integer, db.ForeignKey('places.id'), primary_key=True)
)
# Association table for the many-to-many relationship between user and conversation
conversation_user_association = db.Table('conversation_user_association',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('conversation_id', db.Integer, db.ForeignKey('conversation.id'), primary_key=True)
)
# Association table for the many-to-many relationship between user and follow
follow_user_association = db.Table('follow_user_association',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('follow_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
)
# Creation of our User table 
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
#
    serialize_rules = (
        '-created_at', '-updated_at', '-_password_hash', '-safety_marks.user', 
        '-routes.user', '-reviews', '-followings', '-followers', 
        '-sent_messages', '-received_messages', '-comments', '-notifications.user', 
        '-user_history', '-user_stories'
    )
# Everything each user should have 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password_hash = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.String(500), default='Hi, I am passionate about discovering hidden gems and sharing travel tips from my adventures around the world.')
    image = db.Column(db.String(500), default='https://static.vecteezy.com/system/resources/previews/016/774/588/original/3d-user-icon-on-transparent-background-free-png.png')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    first_name = db.Column(db.String(500), default='John')
    last_name = db.Column(db.String(500), default='Doe')
    location = db.Column(db.String(500), default='Houston, TX')
# Every other table the user is connected to
    safety_marks = db.relationship('SafetyMark', back_populates='user', lazy=True)
    routes = db.relationship('Route', back_populates='user', lazy=True)
    reviews = db.relationship('Review', back_populates='user', lazy=True)
    comments = db.relationship('Comment', back_populates='user', lazy=True)  
    notifications = db.relationship('Notification', back_populates='user', lazy=True)
    history = db.relationship('History', back_populates='user', lazy=True)
    stories = db.relationship('Story', back_populates='user', lazy=True)
    
# Many-to-many self-referential relationships
    following = db.relationship(
        'User',
        secondary=follow_user_association,
        primaryjoin=id==follow_user_association.c.user_id,
        secondaryjoin=id==follow_user_association.c.follow_id,
        backref=db.backref('followers', lazy='dynamic'),
        lazy='dynamic'
    )
  
    sent_messages = db.relationship('Message', foreign_keys='Message.sender_id', back_populates='sender', lazy='dynamic')
    received_messages = db.relationship('Message', foreign_keys='Message.recipient_id', back_populates='recipient', lazy='dynamic')
# Validations for username and emails address
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
# Hashing the password so you can not see it on the backend and making it safter for the user login
    
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
#
    def __repr__(self):
        return f'<User id={self.id} username={self.username} >'
# Creation of our Place table 
class Place(db.Model, SerializerMixin):
    __tablename__ = 'places'
#
    serialize_rules = ('-reviews', '-safety_marks','-routes')
# Everything each place should have 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    safety_rating = db.Column(db.Float, nullable=False)
# Every other table the place is connected to
    reviews = db.relationship('Review', back_populates='place', lazy=True)
    safety_marks = db.relationship('SafetyMark', back_populates='place', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'address': self.address,
            'safety_rating': self.safety_rating
        }
# Validations for naming and saftey ratings    
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
#
    def __repr__(self):
        return f'<Place id={self.id} name={self.name} city={self.city}>'
# Creation of our Route table 
class Route(db.Model, SerializerMixin):
    __tablename__ = 'routes'
#
    serialize_rules = ('-places', '-user')
# Everything each route should have 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# Every other table the route is connected to
    places = db.relationship('Place', secondary=route_place_association, backref=db.backref('routes', lazy='dynamic'))
    user = db.relationship('User', back_populates='routes')
#
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'user_id': self.user_id,
            'places': [place.to_dict() for place in self.places]
        }
# Validations for naming
    @validates('name')
    def validate_name(self, key, name):
        if not name or len(name) < 3:
            raise ValueError('Name must be at least 3 characters long')
        return name 
#
    def __repr__(self):
        return f'<Route id={self.id} name={self.name} user_id={self.user_id} place_id={self.place_id}>'
# Creation of our Review table 
class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
#
    serialize_rules = ('-place.reviews', '-user.reviews', '-review_comments', '-review_likes')
# Everything each review should have
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(500))
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
# Every other table the review is connected to
    place = db.relationship('Place', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews') 
    likes = db.relationship('Like', back_populates='review', lazy=True,)
    comments = db.relationship('Comment', back_populates='review', lazy=True, cascade='all, delete-orphan')
#
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
# Validations for content and rating
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
#
    def __repr__(self):
        return f'<Review id={self.id} rating={self.rating} place_id={self.place_id} user_id={self.user_id}  image={self.image} likes={self.likes} comments={self.comments}>'
# Creation of our Like table 
class Like(db.Model, SerializerMixin):
    __tablename__ = 'likes'
#
    serialize_rules =()
# Everything each like should have 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=False)
    liked_at = db.Column(db.DateTime, default=datetime.utcnow)
# Every other table the like is connected to
    user = db.relationship('User', backref='user_likes')
    review = db.relationship('Review', back_populates='likes')
#
    def __repr__(self):
            return f'<Like id={self.id} user_id={self.user_id} review_id={self.review_id}>'
# Creation of our Safey Marks table
class SafetyMark(db.Model, SerializerMixin):
    __tablename__ = 'safetymarks'
#
    serialize_rules = ('-place.safety_marks', '-user.safety_marks')
# Everything each saftey mark should have 
    id = db.Column(db.Integer, primary_key=True)
    is_safe = db.Column(db.Boolean, nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
# Every other table the saftey mark is connected to
    place = db.relationship('Place', back_populates='safety_marks')
    user = db.relationship('User', back_populates='safety_marks')
# Validations for is_safe mark
    @validates('is_safe')
    def validate_is_safe(self, key, is_safe):
        if not isinstance(is_safe, bool):
            raise ValueError('is_safe must be a boolean')
        return is_safe
#
    def __repr__(self):
        return f'<SafetyMark id={self.id} is_safe={self.is_safe} place_id={self.place_id} user_id={self.user_id}>'

# Creation of our Comment table 
class Comment(db.Model, SerializerMixin):
    __tablename__ = 'comments'
#
    serialize_rules = ('-review.review_comments', '-user.user_comments')
# Everything each comment should have 
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey('reviews.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
# Every other table the comment is connected to
    user = db.relationship('User', back_populates='comments')
    review = db.relationship('Review', back_populates='comments')
#
    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'user_id': self.user_id,
            'review_id': self.review_id,
            'timestamp': self.timestamp
        }
#
def __repr__(self):
        return f'<Comment id={self.id} user_id={self.user_id} review_id={self.review_id}>'
# Creation of our Message table 
class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'
#
    serialize_rules = ('-sender', '-recipient', '-conversation')
# Everything each message should have 
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
# Every other table the message is connected to
    sender = db.relationship('User', foreign_keys=[sender_id], back_populates='sent_messages')
    recipient = db.relationship('User', foreign_keys=[recipient_id], back_populates='received_messages')
    conversation = db.relationship('Conversation', backref='messages')
#
def __repr__(self):
        return f'<Message id={self.id} recipient_id={self.recipient_id} sender_id={self.sender_id}>'
# Creation of our Conversation table 
class Conversation(db.Model, SerializerMixin):
    __tablename__ = 'conversation'
#
    serialize_rules = ('-sender', '-recipient', '-messages')
# Everything each conversation should have 
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
# Every other table the conversation is connected to
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_conversations')
    recipient = db.relationship('User', foreign_keys=[recipient_id], backref='received_conversations')
#
def __repr__(self):
       return f'<Conversation id={self.id} sender_id={self.sender_id} recipient_id={self.recipient_id}>'
# Creation of our Notification table 
class Notification(db.Model, SerializerMixin):
    __tablename__ = 'notifications'
#
    serialize_rules = ('-user.notifications')
# Everything each notification should have 
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(500), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
# Every other table the notification is connected to
    user = db.relationship('User', back_populates='notifications')
#
def to_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'timestamp': self.timestamp,
            'user_id': self.user_id
        }
#
def __repr__(self):
        return f'<Notification id={self.id} message={self.message} user_id={self.user_id} content={self.content[:20]}>'
# Creation of our History table 
class History(db.Model, SerializerMixin):
    __tablename__ = 'history'
#
    serialize_rules = ('-user_history')
# Everything each notification should have
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
# Every other table the notification is connected to
    user = db.relationship('User', back_populates='history')
#
def __repr__(self):
        return f'<History id={self.id} user_id={self.user_id} action={self.action[:20]}>'
# Creation of our Follow table 
class Follow(db.Model, SerializerMixin):
    __tablename__ = 'follows'
#
    serialize_rules = ()   
# Everything each follow should have
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    following_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#
    def __repr__(self):
        return f'<Follow id={self.id} follower_id={self.follower_id} following_id={self.following_id}>'
# Creation of our Story table 
class Story(db.Model, SerializerMixin):
    __tablename__ = 'stories'
#
    serialize_rules = ('user_stories')
# Everything each story should have
    id = db.Column(db.Integer, primary_key=True)
    media = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
# Every other table the story is connected to
    user = db.relationship('User', back_populates='stories')
#
    def to_dict(self):
        return {
            'id': self.id,
            'media': self.media,
            'user_id': self.user_id
        }
#
    def __repr__(self):
        return f'<Story id={self.id} media={self.media} user_id={self.user_id}>'

