

# Import routes after initializing the extensions

# from flask import request, jsonify
from flask import Flask, request, jsonify, session, make_response
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import emit
from config import db, bcrypt, socketio, api, app
from models import User, Place, Route, Review, SafetyMark
from sqlalchemy.exc import SQLAlchemyError


# Initialize extensions with the app instance

# Register Resource
class Register(Resource):
    def post(self):
        params = request.json
        try:
            user = User(username=params.get('username'), email=params.get('email'))
        
            user.password_hash = (params.get('password'))
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            return make_response(user.to_dict(), 201)
        except Exception as e:
            db.session.rollback()
            return make_response({'error': 'something went wrong'}, 400)

api.add_resource(Register, '/api/register')

class CheckSession(Resource):
    def get(self):
        user_id = session.get('user_id')
        if user_id:
            # user = db.session.get(User, user_id)
            user = User.query.get(user_id)
            if user:
                return make_response(user.to_dict(), 200)
        return make_response({'error': 'Unauthorized: Must login'}, 401)

api.add_resource(CheckSession, '/check_session')

class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        # session.pop('user_id', None)
        return make_response({}, 204)

api.add_resource(Logout, '/logout')

class Login(Resource):
    def post(self):
       
        params = request.json
        user = User.query.filter_by(username=params.get('username')).first()
        if not user:
            return make_response({'error': 'user not found'}, 404)
        
        if user.authenticate( params.get('password')):
            session['user_id'] = user.id
            return make_response(user.to_dict(),200)
        else:
            return make_response({'error': 'invalid password' }, 401)

api.add_resource(Login, '/api/login')

import logging

@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())
    app.logger.debug('Session: %s', session)

# Profile Resource
class Profile(Resource):
    def get(self): 
        import ipdb; ipdb.set_trace()
        if 'user_id' not in session:
            return make_response({'error': 'Unauthorized access'}, 401)
        
        user = User.query.get(session['user_id'])
        if not user:
            return make_response({'error': 'User not found'}, 404)
        
        return make_response({
            'username': user.username,
            'email': user.email,
            'bio': user.bio,
            'image': user.image
        })

    def put(self):
        
        if 'user_id' not in session:
            return make_response(({'error': 'Unauthorized access'}), 401)

        user = User.query.get(session['user_id'])
        if not user:
            return make_response(({'error': 'User not found'}), 404)

        data = request.get_json()

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
            return make_response(({'message': 'Profile updated successfully'}), 200)

        except KeyError as e:
            return make_response(({'error': f'Missing key: {str(e)}'}), 400)

        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response(({'error': str(e)}), 500)

        except Exception as e:
            return make_response(({'error': str(e)}), 500)

api.add_resource(Profile, '/api/profile')

# Places Resource
class Places(Resource):
    def get(self):
        places = Place.query.all()
        places_list = [place.to_dict() for place in places]
        return make_response(places_list, 200)

    def post(self):
        data = request.json
        try:
            place = Place(
                name=data['name'],
                city=data['city'],
                address=data['address'],
                safety_rating=data['safety_rating']
            )

            db.session.add(place)
            db.session.commit()

            return make_response(place.to_dict(), 201)
        except Exception as e:
            db.session.rollback()
            return make_response({'error': "couldn't create place"}, 400)

api.add_resource(Places, '/api/places')

# PlaceById Resource
class PlaceById(Resource):
    def get(self, place_id):
        place = Place.query.get_or_404(place_id)
        return make_response((place.to_dict()))
    
  
    def delete(self, place_id):
        place = Place.query.get_or_404(place_id)
        try:
            db.session.delete(place)
            db.session.commit()
            return '', 204
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response({'error': str(e)}, 400)
    # def delete(self, place_id):
    #     if 'user_id' not in session:
    #         return jsonify({'error': 'Unauthorized access'}), 401
        
    #     place = Place.query.get(place_id)
    #     if not place:
    #         return jsonify({'error': 'Place not found'}), 404
        
    #     try:
    #         db.session.delete(place)
    #         db.session.commit()
    #         return make_response({'message': 'Place deleted successfully'}, 200)
    #     except SQLAlchemyError as e:
    #         db.session.rollback()
    #         return make_response({'error': str(e)}, 500)
    #     except Exception as e:
    #         return make_response({'error': str(e)}, 500)

api.add_resource(PlaceById, '/api/places/<int:place_id>')

# Routes Resource
class Routes(Resource):
    def get(self):
        routes = Route.query.all()
        routes_list = [route.to_dict() for route in routes]
        return make_response(routes_list, 200)
     
    def post(self):
        data = request.json
        print("Received data:", data)
        
        if not data:
            return make_response({'error': 'No data provided'}, 400)
        
        if 'name' not in data or 'place_ids' not in data:
            return make_response({'error': 'Missing required fields: name and place_ids'}, 400)
        
        # Assign a default user_id
        user_id = 1  # Default user_id, change as needed
        
        new_route = Route(name=data['name'], user_id=user_id)
        
        # Add the new_route to the session before appending places
        db.session.add(new_route)
        
        for place_id in data['place_ids']:
            place = db.session.get(Place, place_id)  # Use session.get() instead of query.get()
            if place:
                new_route.places.append(place)
        
        try:
            db.session.commit()
            return make_response(jsonify(new_route.to_dict()), 201)
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response({'error': str(e)}, 400)


api.add_resource(Routes, '/api/routes')

class RouteById(Resource):
    def get(self, route_id):
        route = Route.query.get_or_404(route_id)
        return make_response((route.to_dict()))
    
  
    def delete(self, route_id):
        route = Route.query.get_or_404(route_id)
        try:
            db.session.delete(route)
            db.session.commit()
            return '', 204
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response({'error': str(e)}, 400)

api.add_resource(RouteById, '/api/routes/<int:route_id>')

# SafetyMarks Resource
class SafetyMarks(Resource):
    def post(self):
        data = request.get_json()
        user_id = session.get('user_id')
        if not user_id:
            return make_response({'error': 'Unauthorized access'}, 401)

        new_safety_mark = SafetyMark(
            is_safe=data['is_safe'],
            place_id=data['place_id'],
            user_id=user_id
        )
        try:
            db.session.add(new_safety_mark)
            db.session.commit()
            return make_response(new_safety_mark.to_dict(), 201)
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response({'error': str(e)}, 400)

api.add_resource(SafetyMarks, '/api/safety_marks')

# MarkPlaceSafe Resource
class MarkPlaceSafe(Resource):
    def post(self, place_id):
        data = request.get_json()
        is_safe = data.get('is_safe')

        user_id = session.get('user_id')
        if not user_id:
            return make_response({'error': 'Unauthorized access'}, 401)

        safety_mark = SafetyMark(is_safe=is_safe, place_id=place_id, user_id=user_id)
        try:
            db.session.add(safety_mark)
            db.session.commit()
            return make_response({'message': 'Place marked successfully'}, 201)
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response({'error': str(e)}, 400)

api.add_resource(MarkPlaceSafe, '/api/places/<int:place_id>/mark_safe')

# SafetyMarkById Resource
class SafetyMarkById(Resource):
    def delete(self, safety_mark_id):
        safety_mark = SafetyMark.query.get_or_404(safety_mark_id)
        try:
            db.session.delete(safety_mark)
            db.session.commit()
            return '', 204
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response({'error': str(e)}, 400)

api.add_resource(SafetyMarkById, '/api/safety_marks/<int:safety_mark_id>')

# Reviews Resource
class Reviews(Resource):

    def get(self):
        reviews = Review.query.all()
        review_list = [review.to_dict() for review in reviews]
        return make_response((review_list), 200)
    
    def post(self):
        data = request.get_json()
        user_id = session.get('user_id')
        if not user_id:
            return make_response({'error': 'Unauthorized access'}, 401)

        user = User.query.get(user_id)
        if not user:
            return make_response({'error': 'User not found'}, 404)

        new_review = Review(
            content=data['content'],
            rating=data['rating'],
            place_id=data['place_id'],
            user_id=user_id,
            user_name=user.username,
            user_image=user.image
        )
        try:
            db.session.add(new_review)
            db.session.commit()
            return jsonify(new_review.to_dict()), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response({'error': str(e)}, 400)

api.add_resource(Reviews, '/api/reviews')

# ReviewById Resource
class ReviewById(Resource):
    def delete(self, review_id):
        review = Review.query.get_or_404(review_id)
        try:
            db.session.delete(review)
            db.session.commit()
            return '', 204
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response({'error': str(e)}, 400)

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

