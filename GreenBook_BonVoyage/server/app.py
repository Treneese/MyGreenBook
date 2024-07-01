#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, Flask, jsonify, request, make_response, session, render_template
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO, send, emit
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from werkzeug.security import generate_password_hash, check_password_hash
# from mapbox import Geocoder
from sqlalchemy.exc import SQLAlchemyError

from config import db, app, api, socketio, jwt, migrate, CORS

# geocoder = Geocoder(access_token='sk.eyJ1IjoidHJlbmVlc2U5NyIsImEiOiJjbHh4dnFsN2ExZDJhMmtwdmtkbDl4dG45In0.vCYN3WxxmO06CZpe_pqHVQ')
from models import User, Place, Route, Review, SafetyMark


# Models import

# Views go here!
# routes.py

class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201

api.add_resource(Register, '/register')

class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        try:
            user = User.query.filter_by(email=email).first()

            if not user or not user.check_password(password):
                return jsonify({'error': 'Invalid credentials'}), 401

            access_token = create_access_token(identity={'email': user.email})
            return jsonify({'token': access_token}), 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500

api.add_resource(Login, '/login')

class Profile(Resource):
    @jwt_required()
    def get(self):
        user_email = get_jwt_identity()['email']
        user = User.query.filter_by(email=user_email).first_or_404()
        return jsonify({
            'username': user.username,
            'email': user.email,
            'bio': user.bio,
            'image': user.image
        })

    @jwt_required()
    def put(self):
        user_email = get_jwt_identity()['email']
        user = User.query.filter_by(email=user_email).first_or_404()
        data = request.get_json()

        # Validate and update user fields
        try:
            if 'username' in data:
                user.username = data['username']
            if 'email' in data:
                user.email = data['email']
            if 'bio' in data:
                user.bio = data['bio']
            if 'image' in data:
                user.image = data['image']

            db.session.commit()
            return jsonify({'message': 'Profile updated successfully'}), 200

        except KeyError as e:
            return jsonify({'error': f'Missing key: {str(e)}'}), 400
        
        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500

api.add_resource(Profile, '/api/profile')

class Places(Resource):
    @jwt_required()
    def get(self):
        places = Place.query.all()
        return jsonify([place.to_dict() for place in places])

    @jwt_required()
    def post(self):
        data = request.get_json()
        name = data.get('name')
        city = data.get('city')
        address = data.get('address')
        safety_rating = data.get('safety_rating')

        place = Place(name=name, city=city, address=address, safety_rating=safety_rating)
        db.session.add(place)
        db.session.commit()

        return jsonify({'message': 'Place added successfully'}), 201

api.add_resource(Places, '/places')

class PlaceById(Resource):
    @jwt_required()
    def get(self, place_id):
        place = Place.query.get_or_404(place_id)
        return jsonify(place.to_dict())

api.add_resource(PlaceById, '/places/<int:place_id>')

class Routes(Resource):
    @jwt_required()
    def get(self):
        user_email = get_jwt_identity()['email']
        user = User.query.filter_by(email=user_email).first_or_404()
        routes = Route.query.filter_by(user_id=user.id).all()
        return jsonify([route.to_dict() for route in routes])

    @jwt_required()
    def post(self):
        user_email = get_jwt_identity()['email']
        user = User.query.filter_by(email=user_email).first_or_404()
        data = request.get_json()
        new_route = Route(name=data['name'], user_id=user.id)
        for place_id in data['place_ids']:
            place = Place.query.get(place_id)
            if place:
                new_route.places.append(place)
        db.session.add(new_route)
        db.session.commit()
        return jsonify(new_route.to_dict()), 201

api.add_resource(Routes, '/api/routes')

class SafetyMarks(Resource):
    @jwt_required()
    def post(self):
        user_email = get_jwt_identity()['email']
        user = User.query.filter_by(email=user_email).first_or_404()
        data = request.get_json()
        new_safety_mark = SafetyMark(
            is_safe=data['is_safe'],
            place_id=data['place_id'],
            user_id=user.id
        )
        db.session.add(new_safety_mark)
        db.session.commit()
        return jsonify(new_safety_mark.to_dict()), 201

api.add_resource(SafetyMarks, '/api/safety_marks')

class MarkPlaceSafe(Resource):
    @jwt_required()
    def post(self, place_id):
        data = request.get_json()
        is_safe = data.get('is_safe')

        user_email = get_jwt_identity()['email']
        user = User.query.filter_by(email=user_email).first()

        safety_mark = SafetyMark(is_safe=is_safe, place_id=place_id, user_id=user.id)
        db.session.add(safety_mark)
        db.session.commit()

        return jsonify({'message': 'Place marked successfully'}), 201

api.add_resource(MarkPlaceSafe, '/places/<int:place_id>/mark_safe')

class SafetyMarkById(Resource):
    @jwt_required()
    def delete(self, safety_mark_id):
        safety_mark = SafetyMark.query.get_or_404(safety_mark_id)
        db.session.delete(safety_mark)
        db.session.commit()
        return '', 204

api.add_resource(SafetyMarkById, '/api/safety_marks/<int:safety_mark_id>')

class Reviews(Resource):
    @jwt_required()
    def post(self):
        user_email = get_jwt_identity()['email']
        user = User.query.filter_by(email=user_email).first_or_404()
        data = request.get_json()
        new_review = Review(
            content=data['content'],
            rating=data['rating'],
            place_id=data['place_id'],
            user_id=user.id
        )
        db.session.add(new_review)
        db.session.commit()
        return jsonify(new_review.to_dict()), 201

api.add_resource(Reviews, '/api/reviews')

class ReviewById(Resource):
    @jwt_required()
    def delete(self, review_id):
        review = Review.query.get_or_404(review_id)
        db.session.delete(review)
        db.session.commit()
        return '', 204

api.add_resource(ReviewById, '/api/reviews/<int:review_id>')

# Index route
@app.route('/')
def index():
    return "Index for Route/Review/User/SafetyMark/Place API"


# SocketIO events
@socketio.on('message')
def handle_message(msg):
    print('Message:', msg)
    emit('response', {'data': 'Message received!'}, broadcast=True)

if __name__ == '__main__':
    app.run(port=5555, debug=True)