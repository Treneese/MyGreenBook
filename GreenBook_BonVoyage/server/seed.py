# from datetime import datetime
# from config import bcrypt
# from app import app, db
# from models import User, Place, Route, Review, SafetyMark, Comment

# # def seed_users():
# #     try:
# #         ayanna = User(username='ayanna', email='ayanna@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'), image="https://static-00.iconduck.com/assets.00/user-icon-1024x1024-dtzturco.png")
# #         zuri = User(username='zuri', email='zuri@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),  image='https://static-00.iconduck.com/assets.00/user-icon-1024x1024-dtzturco.png')
# #         ezra = User(username='ezra', email='ezra@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),  image='https://static-00.iconduck.com/assets.00/user-icon-1024x1024-dtzturco.png')

# #         db.session.add(ayanna)
# #         db.session.add(zuri)
# #         db.session.add(ezra)
# #         db.session.commit()
# #         print("Users seeded successfully!")
# #     except Exception as e:
# #         print(f"Error seeding user: {e}")

# # def seed_places():
# #     try:
# #         place1 = Place(name='Kwame Nkrumah Memorial Park & Mausoleum', city='Accra', address='GQVV+9M8, Accra, Ghana', safety_rating=4.5)
# #         place2 = Place(name='Black Cultural Archivesy', city='London', address='1 Windrush Square, London SW2 1EF, United Kingdom', safety_rating=4.7)
# #         place3 = Place(name='La Chèvre d’Or', city='Eze', address='Rue du Barri, 06360 Èze, France', safety_rating=4.3)
        
# #         # db.session.add(place1)
# #         # db.session.add(place2)
# #         # db.session.add(place3)
# #         # db.session.commit()
# #         print("Places seeded successfully!")
# #     except Exception as e:
# #         print(f"Error seeding place: {e}")

# # def seed_routes():
# #     try:
# #         place1 = Place.query.filter_by(name='Kwame Nkrumah Memorial Park & Mausoleum').first()
# #         place2 = Place.query.filter_by(name='Black Cultural Archivesy').first()
# #         place3 = Place.query.filter_by(name='La Chèvre d’Or').first()

# #         routes = [
# #             {"name": "Tour of Accra", "user_id": 1, "place_ids": [place1.id, place2.id]},
# #             {"name": "London Highlights", "user_id": 2, "place_ids": [place2.id, place3.id]},
# #             {"name": "Eze's Wonders", "user_id": 3, "place_ids": [place3.id, place1.id]},
# #         ]
        
# #         for route_data in routes:
# #             try:
# #                 route = Route(
# #                     name=route_data["name"],
# #                     user_id=route_data["user_id"]
# #                 )
# #                 for place_id in route_data["place_ids"]:
# #                     place = Place.query.get(place_id)
# #                     if place:
# #                         route.places.append(place)
# #                     else:
# #                         print(f"Error seeding route {route_data['name']}: Place with id {place_id} not found")
# #                 # db.session.add(route)
# #             except Exception as e:
# #                 print(f"Error seeding route {route_data['name']}: {e}")
# #         # db.session.commit()
# #         print("Routes seeded successfully!")
# #     except Exception as e:
# #         print(f"Error seeding routes: {e}")

# def seed_reviews():
#     reviews = [
#         {
#             "content": "Great place!",
#             "rating": 4.7,
#             "place_id": 1,
#             "user_id": 1,
#         },
#         {
#             "content": "Amazing experience!",
#             "rating": 4.5,
#             "place_id": 2,
#             "user_id": 2,
#         },
#         {
#             "content": "A must-visit!",
#             "rating": 4,
#             "place_id": 3,
#             "user_id": 3,
#         },
#     ]

#     with app.app_context():
#         for review_data in reviews:
#             try:
#                 review = Review(
#                     content=review_data["content"],
#                     rating=review_data["rating"],
#                     place_id=review_data["place_id"],
#                     user_id=review_data["user_id"],
#                     created_at=datetime.utcnow()
#                 )
#                 db.session.add(review)
#             # except Exception as e:
#             #     print(f"Error seeding review for place_id {review_data['place_id']}: {e}")
#         db.session.commit()
#         # print("Reviews seeded successfully!")
#                     for _ in range(3):  # Example: Add 3 likes for each review
#                 review.likes += 1
#                 db.session.commit()

#             # Add comments for each review
#             for _ in range(2):  # Example: Add 2 comments for each review
#                 comment = Comment(
#                     content=f"Comment on {review_data['content']}",
#                     user_id=review_data["user_id"],
#                     review_id=review.id
#                 )
#                 db.session.add(comment)
#                 db.session.commit()

#         print("Reviews, likes, and comments seeded successfully!")
#     except Exception as e:
#         print(f"Error seeding reviews, likes, and comments: {e}")


# # def seed_safety_marks():
# #     safety_marks = [
# #         {"is_safe": True, "place_id": 1, "user_id": 1},
# #         {"is_safe": False, "place_id": 2, "user_id": 2},
# #         {"is_safe": True, "place_id": 3, "user_id": 3},
# #     ]
# #     with app.app_context():
# #         for safety_mark_data in safety_marks:
# #             try:
# #                 safety_mark = SafetyMark(
# #                     is_safe=safety_mark_data["is_safe"],
# #                     place_id=safety_mark_data["place_id"],
# #                     user_id=safety_mark_data["user_id"],
# #                     created_at=datetime.utcnow()
# #                 )
# #                 # db.session.add(safety_mark)
# #             except Exception as e:
# #                 print(f"Error seeding safety mark for place_id {safety_mark_data['place_id']}: {e}")
# #         # db.session.commit()
# #         print("Safety marks seeded successfully!")

# # def seed_all():
# #     with app.app_context():
# #         # db.drop_all()
# #         # db.create_all()
# #         recreate_users_table()
# #         recreate_reviews_table()
# #         # seed_users()
# #         # seed_places()
# #         # seed_routes()
# #         # seed_reviews()
# #         # seed_safety_marks()
# #         print("Database seeded!")
# # def recreate_users_table():
#     # with app.app_context():
#     #     # Drop the User table
#     #     User.__table__.drop(db.engine)
#     #     print("User table dropped.")
        
#     #     # Recreate the User table
#     #     db.create_all()
#     #     print("User table created.")

#         # Seed the users
#         # seed_users()

# def recreate_reviews_table():
#     with app.app_context():
#         # Drop the Review table
#         Review.__table__.drop(db.engine)
#         print("Review table dropped.")
        
#         # Recreate the Review table
#         db.create_all()
#         print("Review table created.")

#         # Seed the reviews
#         seed_reviews()

# def seed_all():
#     with app.app_context():
#         # Uncomment below to drop and recreate all tables
#         # db.drop_all()
#         # db.create_all()

#         # Uncomment below to drop and recreate only User and Review tables
#         recreate_users_table()
#         # recreate_reviews_table()

#         # Uncomment below to seed other tables as needed
#         # seed_places()
#         # seed_routes()
#         # seed_safety_marks()

#         print("Database seeded!")

# if __name__ == '__main__':
#     seed_all()


from datetime import datetime
from app import app, db
from models import Review, Comment

def seed_reviews_with_likes_and_comments():
    reviews_data = [
        {
            "content": "Great place!",
            "rating": 4.7,
            "place_id": 1,
            "user_id": 1,
        },
        {
            "content": "Amazing experience!",
            "rating": 4.5,
            "place_id": 2,
            "user_id": 2,
        },
        {
            "content": "A must-visit!",
            "rating": 4,
            "place_id": 3,
            "user_id": 3,
        },
    ]

    try:
        with app.app_context():
            for review_data in reviews_data:
                review = Review(
                    content=review_data["content"],
                    rating=review_data["rating"],
                    place_id=review_data["place_id"],
                    user_id=review_data["user_id"],
                    created_at=datetime.utcnow(),
                    likes=0  # Initialize likes if necessary
                )
                db.session.add(review)
                db.session.commit()

                # Example: Add 3 likes for each review
                for _ in range(3):
                    review.likes += 1
                    db.session.commit()

                # Add comments for each review
                for _ in range(2):
                    comment = Comment(
                        content=f"Comment on {review_data['content']}",
                        user_id=review_data["user_id"],
                        review_id=review.id
                    )
                    db.session.add(comment)
                    db.session.commit()

            print("Reviews, likes, and comments seeded successfully!")

    except Exception as e:
        print(f"Error seeding reviews, likes, and comments: {e}")

if __name__ == '__main__':
    seed_reviews_with_likes_and_comments()
