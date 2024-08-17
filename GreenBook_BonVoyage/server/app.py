

# Import routes after initializing the extensions

# from flask import request, jsonify
from flask import Flask, request, jsonify, session, make_response
from flask_restful import Resource
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import emit
from config import db, bcrypt, socketio, api, app
from models import User, Place, Route, Review, SafetyMark, Comment, Follow, History, Notification, Message
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
        # import ipdb; ipdb.set_trace()
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
        # import ipdb; ipdb.set_trace()
        try:
            db.session.delete(place)
            db.session.commit()
            return '', 204
        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response({'error': str(e)}, 400)
   

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
        # reviews = Review.query.all()
        # review_list = [review.to_dict() for review in reviews]
        # return make_response((review_list), 200)
    
        reviews = Review.query.all()
        reviews_list = []
        for review in reviews:
            review_data = {
                'id': review.id,
                'content': review.content,
                'rating': review.rating,
                'place': {
                    'id': review.place.id,
                    'name': review.place.name
                },
                'user': {
                    'id': review.user.id,
                    'username': review.user.username,
                    'profile_image': review.user.image
                }
            }
            reviews_list.append(review_data)
        return make_response((reviews_list), 200)
    
    def post(self):
        data = request.get_json()
        user_id = session.get('user_id')

        if not user_id:
            return make_response({'error': 'Unauthorized access'}, 401)

        try:
            new_review = Review(
                content=data.get('content'),
                rating=data.get('rating'),
                place_id=data.get('place_id'),
                user_id=user_id
            )

            db.session.add(new_review)
            db.session.commit()

            return make_response(jsonify(new_review.to_dict()), 201)

        except KeyError as e:
            return make_response({'error': f'Missing key: {str(e)}'}, 400)

        except ValueError as e:
            return make_response({'error': str(e)}, 400)

        except SQLAlchemyError as e:
            db.session.rollback()
            return make_response({'error': str(e)}, 500)

        except Exception as e:
            return make_response({'error': str(e)}, 500)

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

# class PlaceByIdReview(Resource):
#     def get(self,review_id):

# api.add_resource(ReviewById, '/api/places/<int:place_id>/reviews')


class LikeReviewById(Resource):
    def post(self, review_id):
        review = Review.query.get_or_404(review_id)
        review.likes += 1
        db.session.commit()
        return make_response({'likes': review.likes}, 200)

api.add_resource(LikeReviewById, '/api/reviews/<int:review_id>/like')


class AddCommentById(Resource):
    def post(self, review_id):
        try:
            data = request.get_json()
            content = data.get('content')
            user_id = data.get('user_id')

            if not content or not user_id:
                return make_response({'error': 'Content and user_id are required'}, 400)

            # Create a new Comment object and add it to the database
            comment = Comment(content=content, user_id=user_id, review_id=review_id)
            db.session.add(comment)
            db.session.commit()

            # Return the new comment data in JSON format
            return make_response(comment.to_dict(), 201)

        except Exception as e:
            return make_response({'error': str(e)}, 500)

# Register the resource with the Flask API
api.add_resource(AddCommentById, '/api/reviews/<int:review_id>/comments')

# class Follow(Resource):
#     def post(self, user_id):
#         follow_user = User.query.get(user_id)
#         follow_user = User.query.get(user_id)
#         if follow_user:
#             current_user = User.query.get(current_user_id)
#             if follow_user not in current_user.following:
#                 current_user.following.append(follow_user)
#                 db.session.commit()
#                 return user_schema.make_response(current_user)
#         return make_response({'message': 'User not found'}), 404

# api.add_resource(Follow, '/follow/<int:user_id>')
class Follow(Resource):
    def post(self, user_id):
        follow_user = User.query.get(user_id)
        if follow_user:
            current_user_id = 1  # Example for demonstration
            current_user = User.query.get(current_user_id)
            if follow_user not in current_user.following:
                current_user.following.append(follow_user)
                db.session.commit()
                return make_response({'user': {'id': current_user.id, 'username': current_user.username}}, 200)
        return make_response({'message': 'User not found'}, 404)
api.add_resource(Follow, '/follow/<int:user_id>')

class Unfollow(Resource):
    def post(self, user_id):
        unfollow_user = User.query.get(user_id)
        if unfollow_user:
            current_user_id = 1  # Example for demonstration
            current_user = User.query.get(current_user_id)
            if unfollow_user in current_user.following:
                current_user.following.remove(unfollow_user)
                db.session.commit()
                return make_response({'user': {'id': current_user.id, 'username': current_user.username}}, 200)
        return make_response({'message': 'User not found'}, 404)
api.add_resource(Unfollow, '/unfollow/<int:user_id>')

class CreatePost(Resource):
    def post(self):
        data = request.get_json()
        current_user_id = 1  # Example for demonstration
        new_post = Post(content=data['content'], user_id=current_user_id)
        db.session.add(new_post)
        db.session.commit()
        return make_response({'post': {'id': new_post.id, 'content': new_post.content}}, 201)
api.add_resource(CreatePost, '/create_post')



class SendMessage(Resource):
    def post(self):
        data = request.get_json()
        current_user_id = 1  # Example for demonstration
        new_message = Message(content=data['content'], sender_id=current_user_id, receiver_id=data['receiver_id'])
        db.session.add(new_message)
        db.session.commit()
        return make_response({'message': {'id': new_message.id, 'content': new_message.content}}, 201)
api.add_resource(SendMessage, '/messages')


class GetHistory(Resource):
    def get(self):
        current_user_id = 1  # Example for demonstration
        history = History.query.filter_by(user_id=current_user_id).all()
        history_list = [{'id': h.id, 'action': h.action, 'timestamp': h.timestamp.isoformat()} for h in history]
        return make_response({'history': history_list}, 200)
api.add_resource(GetHistory, '/history')

class GetNotifications(Resource):
    def get(self):
        current_user_id = 1  # Example for demonstration
        notifications = Notification.query.filter_by(user_id=current_user_id).all()
        notification_list = [{'id': n.id, 'content': n.content, 'timestamp': n.timestamp.isoformat()} for n in notifications]
        return make_response({'notifications': notification_list}, 200)
api.add_resource(GetNotifications, '/notifications')

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

