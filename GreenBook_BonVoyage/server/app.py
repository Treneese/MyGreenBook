# #!/usr/bin/env python3

# # Standard library imports

# # Remote library imports
# from flask import request, Flask, jsonify, request, make_response, session, render_template
# from flask_restful import Resource, Api
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_cors import CORS
# from flask_socketio import SocketIO, send, emit
# # from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager, \
# #     jwt_unauthorized_loader, jwt_expired_token_loader, \
# #     get_raw_jwt, create_access_token
# from flask_jwt_extended import create_access_token
# from werkzeug.security import generate_password_hash, check_password_hash
# # from mapbox import Geocoder
# from sqlalchemy.exc import SQLAlchemyError

# from config import db, app, api, socketio, jwt, migrate, CORS

# # geocoder = Geocoder(access_token='sk.eyJ1IjoidHJlbmVlc2U5NyIsImEiOiJjbHh4dnFsN2ExZDJhMmtwdmtkbDl4dG45In0.vCYN3WxxmO06CZpe_pqHVQ')
# from models import User, Place, Route, Review, SafetyMark
# CORS(app)


# class Register(Resource):
#     def post(self):
#         # params = request.json
#         # try:
#         #     # Create the user with hashed password
#         #     user = User(username=params.get('username'), email=params.get('email'), password=params.get('password'))
#         #     db.session.add(user)
#         #     db.session.commit()
#         #     session['user_id'] = user.id
#         #     return make_response(user.to_dict(), 201)
#         # except Exception as e:
#         #     return make_response({'error': str(e)}, 400)
#         data = request.get_json()
#         username = data.get('username')
#         email = data.get('email')
#         password = data.get('password')
#         user = User(username=username, email=email, password=password)
#         user.set_password(password)
#         db.session.add(user)
#         db.session.commit()
#         return jsonify(message="User registered successfully"), 201



# api.add_resource(Register, '/api/register')

# class CheckSession(Resource):
#     def get(self):
#         user_id = session.get('user_id')
#         if user_id:
#             user = db.session.get(User, user_id)
#             if user:
#                 return make_response(user.to_dict(), 200)
#         return make_response({'error': 'Unauthorized: Must login'}, 401)

# api.add_resource(CheckSession, '/api/check_session')

# class Logout(Resource):
#     def delete(self):
#         session['user_id'] = None
#         return make_response({}, 204)

# api.add_resource(Logout, '/api/logout')

# class Login(Resource):
#     # def post(self):
#     #     params = request.json
#     #     user = User.authenticate(params.get('username'), params.get('password'))
#     #     if not user:
#     #         return make_response({'error': 'Invalid username or password'}, 401)
        
#     #     session['user_id'] = user.id
#     #     return make_response(user.to_dict())

#     def post(self):
#         # params = request.json
#         # user = User.query.filter_by(username=params.get('username')).first()
        
#         # if user:
#         #     print(f"Stored password hash: {user._password_hash}")
        
#         # # Bypass password check (development only)
#         # if user:
#         #     session['user_id'] = user.id
#         #     return make_response(user.to_dict())
#         # else:
#         #     return make_response({'error': 'Invalid username or password'}, 401)

#         params = request.json
#         print('Received login payload:', params)
#         user = User.query.filter_by(username=params.get('username')).first()
#         if user:
#             print('User found:', user)
#             print(f"Stored password hash: {user.password_hash}")
#             print(f"Received password: {params.get('password')}")
#             if user.check_password(params.get('password')):
#                 session['user_id'] = user.id
#                 access_token = create_access_token(identity={'username': user.username})
#                 return make_response(jsonify(access_token=access_token), 200)
#             else:
#                 print('Password mismatch')
#         else:
#             print('User not found')

#         return make_response(jsonify({'error': 'Invalid username or password'}), 401)

#         #     session['user_id'] = user.id
#         #     access_token = create_access_token(identity={'username': user.username})
#         #     return make_response(jsonify(access_token=access_token), 200)
#         # else:
#         #     return make_response(jsonify({'error': 'Invalid username or password'}), 401)


#         # username = request.json.get('username')
#         # password = request.json.get('password')

#         # # Validate username and password (example)
#         # if username == 'admin' and password == 'admin123':
#         #     access_token = create_access_token(identity=username)
#         #     return jsonify(access_token=access_token), 200
#         # else:
#         #     return jsonify({'message': 'Invalid credentials'}), 401
#         # params = request.json
#         # user = User.query.filter_by(username=params.get('username')).first()
    
#         # if user:
#         #     # Debug: Print the stored password hash (development only)
#         #     print(f"Stored password hash: {user.password_hash}")
            
#         #     # Bypass password check (development only)
#         #     # Remove this block in production
#         #     if user:
#         #         session['user_id'] = user.id
#         #         return make_response(jsonify(user.to_dict()), 200)
            
#         # return make_response(jsonify({'error': 'Invalid username or password'}), 401)


# api.add_resource(Login, '/api/login')

# @app.before_request
# def check_authorized():
#     authorized_endpoints = ['profile', 'places', 'routes', 'chat', 'placebyid', 'markplacesafe', 'map']
#     excluded_endpoints = ['login', 'register', 'checksession']

#     endpoint_parts = request.endpoint.split('.') if request.endpoint else []

#     if len(endpoint_parts) == 1 and endpoint_parts[0] in excluded_endpoints:
#         return None

#     if len(endpoint_parts) == 1 and endpoint_parts[0] in authorized_endpoints and not session.get('user_id'):
#         return make_response({'error': 'Unauthorized: Must login'}, 401)

# # @app.route('/api/protected', methods=['GET'])
# # # @jwt_required()
# # def protected():
# #     current_user = get_jwt_identity()
# #     return jsonify(logged_in_as=current_user), 200

# # @jwt_unauthorized_loader
# # def my_unauthorized_loader(callback):
# #     return jsonify({
# #         'status': 'error',
# #         'message': 'Missing Authorization Header'
# #     }), 401

# # @jwt_expired_token_loader
# # def my_expired_token_loader(callback):
# #     return jsonify({
# #         'status': 'error',
# #         'message': 'Token has expired'
# #     }), 401

# class Profile(Resource):
#     # @jwt_required()
#     def get(self):
#         user_email =['email']
#         # get_jwt_identity()
#         # ()['email']
#         user = User.query.filter_by(email=user_email).first_or_404()
#         return jsonify({
#             'username': user.username,
#             'email': user.email,
#             'bio': user.bio,
#             'image': user.image
#         }) 

#     # @jwt_required()
#     def put(self):
#         user_email = ['email']
#         # get_jwt_identit()
#         user = User.query.filter_by(email=user_email).first_or_404()
#         data = request.get_json()

#         # Validate and update user fields
#         try:
#             if 'username' in data:
#                 user.username = data['username']
#             if 'email' in data:
#                 user.email = data['email']
#             if 'bio' in data:
#                 user.bio = data['bio']
#             if 'image' in data:
#                 user.image = data['image']

#             db.session.commit()
#             return jsonify({'message': 'Profile updated successfully'}), 200

#         except KeyError as e:
#             return jsonify({'error': f'Missing key: {str(e)}'}), 400
        
#         except SQLAlchemyError as e:
#             db.session.rollback()
#             return jsonify({'error': str(e)}), 500

#         except Exception as e:
#             return jsonify({'error': str(e)}), 500

# api.add_resource(Profile, '/api/profile')

# class Places(Resource):
#     # @jwt_required()
#     def get(self):
#         places = Place.query.all()
#         return jsonify([place.to_dict() for place in places])

#     # @jwt_required()
#     def post(self):
#         data = request.get_json()
#         name = data.get('name')
#         city = data.get('city')
#         address = data.get('address')
#         safety_rating = data.get('safety_rating')

#         place = Place(name=name, city=city, address=address, safety_rating=safety_rating)
#         db.session.add(place)
#         db.session.commit()

#         return jsonify({'message': 'Place added successfully'}), 201

# api.add_resource(Places, '/api/places')

# class PlaceById(Resource):
#     # @jwt_required()
#     def get(self, place_id):
#         place = Place.query.get_or_404(place_id)
#         return jsonify(place.to_dict())

# api.add_resource(PlaceById, '/api/places/<int:place_id>')

# class Routes(Resource):
#     # @jwt_required()
#     def get(self):
#         user_email = ['email']
#         # get_jwt_identity()
#         user = User.query.filter_by(email=user_email).first_or_404()
#         routes = Route.query.filter_by(user_id=user.id).all()
#         return jsonify([route.to_dict() for route in routes])

#     # @jwt_required()
#     def post(self):
#         user_email = ['email']
#         # get_jwt_identity()
#         user = User.query.filter_by(email=user_email).first_or_404()
#         data = request.get_json()
#         new_route = Route(name=data['name'], user_id=user.id)
#         for place_id in data['place_ids']:
#             place = Place.query.get(place_id)
#             if place:
#                 new_route.places.append(place)
#         db.session.add(new_route)
#         db.session.commit()
#         return jsonify(new_route.to_dict()), 201

# api.add_resource(Routes, '/api/routes')

# class SafetyMarks(Resource):
#     # @jwt_required()
#     def post(self):
#         user_email = ['email']
#         # get_jwt_identity()
#         user = User.query.filter_by(email=user_email).first_or_404()
#         data = request.get_json()
#         new_safety_mark = SafetyMark(
#             is_safe=data['is_safe'],
#             place_id=data['place_id'],
#             user_id=user.id
#         )
#         db.session.add(new_safety_mark)
#         db.session.commit()
#         return jsonify(new_safety_mark.to_dict()), 201

# api.add_resource(SafetyMarks, '/api/safety_marks')

# class MarkPlaceSafe(Resource):
#     # @jwt_required()
#     def post(self, place_id):
#         data = request.get_json()
#         is_safe = data.get('is_safe')

#         user_email = ['email']
#         # get_jwt_identity()
#         user = User.query.filter_by(email=user_email).first()

#         safety_mark = SafetyMark(is_safe=is_safe, place_id=place_id, user_id=user.id)
#         db.session.add(safety_mark)
#         db.session.commit()

#         return jsonify({'message': 'Place marked successfully'}), 201

# api.add_resource(MarkPlaceSafe, '/api/places/<int:place_id>/mark_safe')

# class SafetyMarkById(Resource):
#     # @jwt_required()
#     def delete(self, safety_mark_id):
#         safety_mark = SafetyMark.query.get_or_404(safety_mark_id)
#         db.session.delete(safety_mark)
#         db.session.commit()
#         return '', 204

# api.add_resource(SafetyMarkById, '/api/safety_marks/<int:safety_mark_id>')

# class Reviews(Resource):
#     # @jwt_required()
#     def post(self):
#         user_email = ['email']
#         # get_jwt_identity()
#         user = User.query.filter_by(email=user_email).first_or_404()
#         data = request.get_json()
#         new_review = Review(
#             content=data['content'],
#             rating=data['rating'],
#             place_id=data['place_id'],
#             user_id=user.id
#         )
#         db.session.add(new_review)
#         db.session.commit()
#         return jsonify(new_review.to_dict()), 201

# api.add_resource(Reviews, '/api/reviews')

# class ReviewById(Resource):
#     # @jwt_required()
#     def delete(self, review_id):
#         review = Review.query.get_or_404(review_id)
#         db.session.delete(review)
#         db.session.commit()
#         return '', 204

# api.add_resource(ReviewById, '/api/reviews/<int:review_id>')

# # Index route
# @app.route('/')
# def index():
#     return "Index for Route/Review/User/SafetyMark/Place API"


# # SocketIO events
# @socketio.on('message')
# def handle_message(msg):
#     print('Message:', msg)
#     emit('response', {'data': 'Message received!'}, broadcast=True)

# if __name__ == '__main__':
#     app.run(port=5555, debug=True)

# app.py

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
            user = db.session.get(User, user_id)
            if user:
                return make_response(user.to_dict(), 200)
        return make_response({'error': 'Unauthorized: Must login'}, 401)

api.add_resource(CheckSession, '/check_session')

class Logout(Resource):
    def delete(self):
        session['user_id'] = None
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
            return make_response(user.to_dict())
        else:
            return make_response({'error': 'invalid password' }, 401)

api.add_resource(Login, '/api/login')


# Profile Resource
class Profile(Resource):
    def get(self):
        
        user = User.query.get(session['user_id'])
        return jsonify({
            'username': user.username,
            'email': user.email,
            'bio': user.bio,
            'image': user.image
        })

    def put(self):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized access'}), 401

        user = User.query.get(session['user_id'])
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
            return jsonify({'message': 'Profile updated successfully'}), 200

        except KeyError as e:
            return jsonify({'error': f'Missing key: {str(e)}'}), 400

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500

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
        return jsonify(place.to_dict())

api.add_resource(PlaceById, '/api/places/<int:place_id>')

# Routes Resource
class Routes(Resource):
    def get(self):
        routes = Route.query.all()
        routes_list = [route.to_dict() for route in routes]
        return make_response(routes_list, 200)
    
    def post(self):
        data = request.get_json()
        user_id = session.get('user_id')
        if not user_id:
            return make_response({'error': 'Unauthorized access'}, 401)
        
        new_route = Route(name=data['name'], user_id=user_id)
        for place_id in data['place_ids']:
            place = Place.query.get(place_id)
            if place:
                new_route.places.append(place)
        try:
            db.session.add(new_route)
            db.session.commit()
            return make_response(new_route.to_dict(), 201)
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response({'error': str(e)}, 400)

api.add_resource(Routes, '/api/routes')

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
    def post(self):
        data = request.get_json()
        user_id = session.get('user_id')
        if not user_id:
            return make_response({'error': 'Unauthorized access'}, 401)

        new_review = Review(
            content=data['content'],
            rating=data['rating'],
            place_id=data['place_id'],
            user_id=user_id
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


#!/usr/bin/env python3

# Standard library imports

# # Remote library imports
# from flask import request, Flask, jsonify, request, make_response, session, render_template
# from flask_restful import Resource, Api
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_socketio import SocketIO, send, emit
# from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
# from werkzeug.security import generate_password_hash, check_password_hash
# # from mapbox import Geocoder
# from sqlalchemy.exc import SQLAlchemyError

# from config import db, app, api, socketio, jwt, migrate, CORS

# # geocoder = Geocoder(access_token='sk.eyJ1IjoidHJlbmVlc2U5NyIsImEiOiJjbHh4dnFsN2ExZDJhMmtwdmtkbDl4dG45In0.vCYN3WxxmO06CZpe_pqHVQ')
# from models import User, Place, Route, Review, SafetyMark


# # Models import

# # Views go here!
# # routes.py

# class Register(Resource):
#     def post(self):
#         data = request.get_json()
#         username = data.get('username')
#         email = data.get('email')
#         password = data.get('password')

#         if User.query.filter_by(email=email).first():
#             return jsonify({'error': 'Email already exists'}), 400

#         user = User(username=username, email=email)
#         user.password_hash=(password)
#         db.session.add(user)
#         db.session.commit()

#         return jsonify({'message': 'User registered successfully'}), 201

# api.add_resource(Register, '/api/register')

# class Login(Resource):
#     def post(self):
#         data = request.get_json()
#         email = data.get('email')
#         password = data.get('password')

#         try:
#             user = User.query.filter_by(email=email).first()

#             if not user or not user.check_password(password):
#                 return jsonify({'error': 'Invalid credentials'}), 401

#             access_token = create_access_token(identity={'email': user.email})
#             return jsonify({'token': access_token}), 200
#         #make_response user

#         except SQLAlchemyError as e:
#             db.session.rollback()
#             return jsonify({'error': str(e)}), 500

#         except Exception as e:
#             return jsonify({'error': str(e)}), 500

# api.add_resource(Login, '/api/login')

# class Profile(Resource):
#     @jwt_required()
#     def get(self):
#         user_email = get_jwt_identity()['email']
#         user = User.query.filter_by(email=user_email).first_or_404()
#         return jsonify({
#             'username': user.username,
#             'email': user.email,
#             'bio': user.bio,
#             'image': user.image
#         })

#     @jwt_required()
#     def put(self):
#         user_email = get_jwt_identity()['email']
#         user = User.query.filter_by(email=user_email).first_or_404()
#         data = request.get_json()

#         # Validate and update user fields
#         try:
#             if 'username' in data:
#                 user.username = data['username']
#             if 'email' in data:
#                 user.email = data['email']
#             if 'bio' in data:
#                 user.bio = data['bio']
#             if 'image' in data:
#                 user.image = data['image']

#             db.session.commit()
#             return jsonify({'message': 'Profile updated successfully'}), 200

#         except KeyError as e:
#             return jsonify({'error': f'Missing key: {str(e)}'}), 400
        
#         except SQLAlchemyError as e:
#             db.session.rollback()
#             return jsonify({'error': str(e)}), 500

#         except Exception as e:
#             return jsonify({'error': str(e)}), 500

# api.add_resource(Profile, '/api/profile')

# class Places(Resource):
#     @jwt_required()
#     def get(self):
#         places = Place.query.all()
#         return jsonify([place.to_dict() for place in places])


#     @jwt_required()
#     def post(self):
#         data = request.get_json()
#         name = data.get('name')
#         city = data.get('city')
#         address = data.get('address')
#         safety_rating = data.get('safety_rating')

#         # place = Place(name=name, city=city, address=address, safety_rating=safety_rating)
#         places = {
#             'name': name,
#             'city': city,
#             'address': address,
#             'safety_rating': safety_rating
#         }
#         db.session.add(places)
#         db.session.commit()

#         return jsonify({'message': 'Place added successfully'}), 201

# api.add_resource(Places, '/api/places')

# class PlaceById(Resource):
#     @jwt_required()
#     def get(self, place_id):
#         place = Place.query.get_or_404(place_id)
#         return jsonify(place.to_dict())

# api.add_resource(PlaceById, '/api/places/<int:place_id>')

# class Routes(Resource):
#     @jwt_required()
#     def get(self):
#         user_email = get_jwt_identity()['email']
#         user = User.query.filter_by(email=user_email).first_or_404()
#         routes = Route.query.filter_by(user_id=user.id).all()
#         return jsonify([route.to_dict() for route in routes])

#     @jwt_required()
#     def post(self):
#         user_email = get_jwt_identity()['email']
#         user = User.query.filter_by(email=user_email).first_or_404()
#         data = request.get_json()
#         new_route = Route(name=data['name'], user_id=user.id)
#         for place_id in data['place_ids']:
#             place = Place.query.get(place_id)
#             if place:
#                 new_route.places.append(place)
#         db.session.add(new_route)
#         db.session.commit()
#         return jsonify(new_route.to_dict()), 201

# api.add_resource(Routes, '/api/routes')

# class SafetyMarks(Resource):
#     @jwt_required()
#     def post(self):
#         user_email = get_jwt_identity()['email']
#         user = User.query.filter_by(email=user_email).first_or_404()
#         data = request.get_json()
#         new_safety_mark = SafetyMark(
#             is_safe=data['is_safe'],
#             place_id=data['place_id'],
#             user_id=user.id
#         )
#         db.session.add(new_safety_mark)
#         db.session.commit()
#         return jsonify(new_safety_mark.to_dict()), 201

# api.add_resource(SafetyMarks, '/api/safety_marks')

# class MarkPlaceSafe(Resource):
#     @jwt_required()
#     def post(self, place_id):
#         data = request.get_json()
#         is_safe = data.get('is_safe')

#         user_email = get_jwt_identity()['email']
#         user = User.query.filter_by(email=user_email).first()

#         safety_mark = SafetyMark(is_safe=is_safe, place_id=place_id, user_id=user.id)
#         db.session.add(safety_mark)
#         db.session.commit()

#         return jsonify({'message': 'Place marked successfully'}), 201

# api.add_resource(MarkPlaceSafe, '/api/places/<int:place_id>/mark_safe')

# class SafetyMarkById(Resource):
#     @jwt_required()
#     def delete(self, safety_mark_id):
#         safety_mark = SafetyMark.query.get_or_404(safety_mark_id)
#         db.session.delete(safety_mark)
#         db.session.commit()
#         return '', 204

# api.add_resource(SafetyMarkById, '/api/safety_marks/<int:safety_mark_id>')

# class Reviews(Resource):
#     @jwt_required()
#     def post(self):
#         user_email = get_jwt_identity()['email']
#         user = User.query.filter_by(email=user_email).first_or_404()
#         data = request.get_json()
#         new_review = Review(
#             content=data['content'],
#             rating=data['rating'],
#             place_id=data['place_id'],
#             user_id=user.id
#         )
#         db.session.add(new_review)
#         db.session.commit()
#         return jsonify(new_review.to_dict()), 201

# api.add_resource(Reviews, '/api/reviews')

# class ReviewById(Resource):
#     @jwt_required()
#     def delete(self, review_id):
#         review = Review.query.get_or_404(review_id)
#         db.session.delete(review)
#         db.session.commit()
#         return '', 204

# api.add_resource(ReviewById, '/api/reviews/<int:review_id>')

# # Index route
# @app.route('/')
# def index():
#     return "Index for Route/Review/User/SafetyMark/Place API"


# # SocketIO events
# @socketio.on('message')
# def handle_message(msg):
#     print('Message:', msg)
#     emit('response', {'data': 'Message received!'}, broadcast=True)

# if __name__ == '__main__':
#     app.run(port=5555, debug=True)