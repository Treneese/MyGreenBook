from datetime import datetime
from config import bcrypt
from app import app, db
from models import User, Place, Route, Review, SafetyMark

def seed_users():
    try:
        ayanna = User(username='ayanna', email='ayanna@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'))
        zuri = User(username='zuri', email='zuri@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'))
        ezra = User(username='ezra', email='ezra@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'))

        db.session.add(ayanna)
        db.session.add(zuri)
        db.session.add(ezra)
        db.session.commit()
        print("Users seeded successfully!")
    except Exception as e:
        print(f"Error seeding user: {e}")

def seed_places():
    try:
        place1 = Place(name='Kwame Nkrumah Memorial Park & Mausoleum', city='Accra', address='GQVV+9M8, Accra, Ghana', safety_rating=4.5)
        place2 = Place(name='Black Cultural Archivesy', city='London', address='1 Windrush Square, London SW2 1EF, United Kingdom', safety_rating=4.7)
        place3 = Place(name='La Chèvre d’Or', city='Eze', address='Rue du Barri, 06360 Èze, France', safety_rating=4.3)
        
        db.session.add(place1)
        db.session.add(place2)
        db.session.add(place3)
        db.session.commit()
        print("Places seeded successfully!")
    except Exception as e:
        print(f"Error seeding place: {e}")

def seed_routes():
    try:
        place1 = Place.query.filter_by(name='Kwame Nkrumah Memorial Park & Mausoleum').first()
        place2 = Place.query.filter_by(name='Black Cultural Archivesy').first()
        place3 = Place.query.filter_by(name='La Chèvre d’Or').first()

        routes = [
            {"name": "Tour of Accra", "user_id": 1, "place_ids": [place1.id, place2.id]},
            {"name": "London Highlights", "user_id": 2, "place_ids": [place2.id, place3.id]},
            {"name": "Eze's Wonders", "user_id": 3, "place_ids": [place3.id, place1.id]},
        ]
        
        for route_data in routes:
            try:
                route = Route(
                    name=route_data["name"],
                    user_id=route_data["user_id"]
                )
                for place_id in route_data["place_ids"]:
                    place = Place.query.get(place_id)
                    if place:
                        route.places.append(place)
                    else:
                        print(f"Error seeding route {route_data['name']}: Place with id {place_id} not found")
                db.session.add(route)
            except Exception as e:
                print(f"Error seeding route {route_data['name']}: {e}")
        db.session.commit()
        print("Routes seeded successfully!")
    except Exception as e:
        print(f"Error seeding routes: {e}")

def seed_reviews():
    reviews = [
        {
            "content": "Great place!",
            "rating": 4.7,
            "place_id": 1,
            "user_id": 1,
            "user_name": "Ayanna",
            "user_image": "https://example.com/image1.jpg",
        },
        {
            "content": "Amazing experience!",
            "rating": 4.5,
            "place_id": 2,
            "user_id": 2,
            "user_name": "Zuri",
            "user_image": "https://example.com/image2.jpg",
        },
        {
            "content": "A must-visit!",
            "rating": 4,
            "place_id": 3,
            "user_id": 3,
            "user_name": "Ezra",
            "user_image": "https://example.com/image3.jpg",
        },
    ]

    with app.app_context():
        for review_data in reviews:
            try:
                review = Review(
                    content=review_data["content"],
                    rating=review_data["rating"],
                    place_id=review_data["place_id"],
                    user_id=review_data["user_id"],
                    user_name=review_data["user_name"],
                    user_image=review_data["user_image"],
                    created_at=datetime.utcnow()
                )
                db.session.add(review)
            except Exception as e:
                print(f"Error seeding review for place_id {review_data['place_id']}: {e}")
        db.session.commit()
        print("Reviews seeded successfully!")

def seed_safety_marks():
    safety_marks = [
        {"is_safe": True, "place_id": 1, "user_id": 1},
        {"is_safe": False, "place_id": 2, "user_id": 2},
        {"is_safe": True, "place_id": 3, "user_id": 3},
    ]
    with app.app_context():
        for safety_mark_data in safety_marks:
            try:
                safety_mark = SafetyMark(
                    is_safe=safety_mark_data["is_safe"],
                    place_id=safety_mark_data["place_id"],
                    user_id=safety_mark_data["user_id"],
                    created_at=datetime.utcnow()
                )
                db.session.add(safety_mark)
            except Exception as e:
                print(f"Error seeding safety mark for place_id {safety_mark_data['place_id']}: {e}")
        db.session.commit()
        print("Safety marks seeded successfully!")

def seed_all():
    with app.app_context():
        db.drop_all()
        db.create_all()
        seed_users()
        seed_places()
        seed_routes()
        seed_reviews()
        seed_safety_marks()
        print("Database seeded!")

if __name__ == '__main__':
    seed_all()

