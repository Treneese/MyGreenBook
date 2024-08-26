from datetime import datetime
from config import bcrypt
from app import app, db
from models import User, Place, Conversation, Follower, Following, Follow, History, Notification, Review, Route, SafetyMark, Story, Comment, Message, Like

def seed_users():
    try:
        users = [
            User(username='Ayanna', email='ayanna@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'), image="client/public/profile/pexels-1211979-3444087.jpg"),
            User(username='Zuri', email='zuri@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),  image='client/public/profile/pexels-anastasia-shuraeva-6608313.jpg'),
            User(username='Ezra', email='ezra@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),  image='client/public/profile/pexels-anastasiya-gepp-654466-4382484.jpg'),
            User(username='Lori', email='lori@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'), image="client/public/profile/pexels-emir94x-3796217.jpg"),
            User(username='Jazzy', email='jazzy@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),  image='client/public/profile/pexels-koolshooters-6976943.jpg'),
            User(username='Raina', email='raina@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),  image='client/public/profile/pexels-anna-nekrashevich-8993561.jpg'),
            User(username='Borlan', email='borlan@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'), image="client/public/profile/pexels-michelle-leman-6774998.jpg"),
            User(username='Izzy', email='izzy@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),  image='client/public/profile/pexels-gabby-k-5876695.jpg'),
            User(username='Brass', email='brass@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),  image='client/public/profile/pexels-picturesbyamusan-7745573.jpg'),
            User(username='Dranon', email='dranon@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'), image="client/public/profile/pexels-laker-5792641.jpg"),
            User(username='Yesterday', email='yesterday@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),  image='client/public/profile/pexels-wesleydavi-7116213.jpg'),
            User(username='Hronic', email='hronic@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),  image='client/public/profile/pexels-gabby-k-5384445.jpg'),
            User(username='Blessing', email='blessing@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'), image="client/public/profile/pexels-dziana-hasanbekava-7275385.jpg"),
            User(username='Yibar', email='yibar@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),  image='client/public/profile/pexels-rdne-7148620.jpg'),
            User(username='James', email='james@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),  image='client/public/profile/pexels-cottonbro-5082976.jpg'),
            User(username='Cassey', email='cassey@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'), image="client/public/profile/pexels-arshamhaghani-3445219.jpg"),
            User(username='Wanda', email='wanda@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),  image='client/public/profile/pexels-orlovamaria-4946515.jpg'),
            User(username='Fancy', email='francy@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),  image='client/public/profile/pexels-taina-bernard-1861666-3586091.jpg'),
            User(username='Grace', email='grace@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'), image="client/public/profile/pexels-cottonbro-4937366.jpg"),
            User(username='Just', email='just@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),  image='client/public/profile/pexels-kowalievska-4171757.jpg'),
            User(username='Kindness', email='kindness@example.com', password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),  image='client/public/profile/pexels-gabby-k-6194365.jpg')
        ]
        db.session.bulk_save_objects(users)
        db.session.commit()
        print("Users seeded successfully!")
    except Exception as e:
        print(f"Error seeding users: {e}")

def seed_places():
    try:
        places = [
            Place(name='Kwame Nkrumah Memorial Park & Mausoleum', city='Accra', address='GQVV+9M8, Accra, Ghana', safety_rating=4.5),
            Place(name='Black Cultural Archives', city='London', address='1 Windrush Square, London SW2 1EF, United Kingdom', safety_rating=4.7),
            Place(name='La Chèvre d’Or', city='Eze', address='Rue du Barri, 06360 Èze, France', safety_rating=4.3),
            Place(name='teamLab Borderless: MORI Building DIGITAL ART MUSEUM', city='Tokyo', address='Japan, 〒106-0041 Tokyo, Minato City, Azabudai, 1 Chome−2−4 ヒルズ ガーデンプラザ B B1', safety_rating=4.7),
            Place(name='Moses Mabhida Stadium', city='Durban', address='44 Isaiah Ntshangase Rd, Stamford Hill, Durban, 4023, South Africa', safety_rating=4.6),
            Place(name='Everland', city='Gyeonggi-do', address='199 Everland-ro, Yongin-si, Gyeonggi-do, South Korea', safety_rating=4.3),
            Place(name='Iguazu Falls', city='Argentina', address='Misiones Province, Argentina', safety_rating=4.5),
            Place(name='Market Square Park', city='Huston', address='301 Milam St, Houston, TX 77002', safety_rating=4.7),
            Place(name='Georgia Aquarium', city='Atlanta', address='225 Baker St NW, Atlanta, GA 30313', safety_rating=4.3),
            Place(name='Times Square', city='Manhattan', address='Manhattan, NY 10036', safety_rating=4.5),
            Place(name='Anza-Borrego Desert State Park', city='Borrego Springs', address='4M2X+5F Borrego Springs, California', safety_rating=4.7),
            Place(name='27 Waterfalls of Damajagua', city='Dominican Republic', address='Damajagua 57000, Dominican Republic', safety_rating=4.3),
            Place(name='Blue Hole Mineral Spring', city='Brighton District', address='1 Blue Hole Mineral Spring Road, Brighton District, Jamaica', safety_rating=4.5),
            Place(name='Martha Brae River', city='Jamaica', address='Jamaica', safety_rating=4.7),
            Place(name='Trafalgar Square', city='London', address='Trafalgar Sq, London WC2N 5DS, United Kingdom', safety_rating=4.3)
        ]
        db.session.bulk_save_objects(places)
        db.session.commit()
        print("Places seeded successfully!")
    except Exception as e:
        print(f"Error seeding places: {e}")

def seed_routes():
    try:
        # Ensure places are seeded first
        place1 = Place.query.filter_by(name='Kwame Nkrumah Memorial Park & Mausoleum').first()
        place2 = Place.query.filter_by(name='Black Cultural Archives').first()
        place3 = Place.query.filter_by(name='La Chèvre d’Or').first()
        place4 = Place.query.filter_by(name='teamLab Borderless: MORI Building DIGITAL ART MUSEUM').first()
        place5 = Place.query.filter_by(name='Moses Mabhida Stadium').first()
        place6 = Place.query.filter_by(name='Everland').first()
        place7 = Place.query.filter_by(name='Iguazu Falls').first()
        place8 = Place.query.filter_by(name='Market Square Park').first()
        place9 = Place.query.filter_by(name='Georgia Aquarium').first()
        place10 = Place.query.filter_by(name='Times Square').first()
        place11 = Place.query.filter_by(name='Anza-Borrego Desert State Park').first()
        place12 = Place.query.filter_by(name='27 Waterfalls of Damajagua').first()
        place13 = Place.query.filter_by(name='Blue Hole Mineral Spring').first()
        place14 = Place.query.filter_by(name='Martha Brae River').first()
        place15 = Place.query.filter_by(name='Trafalgar Square').first()

        routes = [
            Route(name="Tour of Accra", user_id=1, places=[place1, place5]),
            Route(name="London Highlights", user_id=2, places=[place2, place3]),
            Route(name="Eze's Wonders", user_id=3, places=[place2, place15]),
            Route(name="Tour of Accra", user_id=6, places=[place10, place9]),
            Route(name="London Highlights", user_id=8, places=[place10, place11]),
            Route(name="Eze's Wonders", user_id=12, places=[place9, place8]),
            Route(name="Tour of Accra", user_id=1, places=[place12, place7]),
            Route(name="London Highlights", user_id=7, places=[place13, place14]),
            Route(name="Eze's Wonders", user_id=16, places=[place12, place14]),
            Route(name="Tour of Accra", user_id=21, places=[place4, place6]),
            Route(name="London Highlights", user_id=2, places=[place7, place8]),
            Route(name="Eze's Wonders", user_id=3, places=[place9, place11])
        ]

        db.session.bulk_save_objects(routes)
        db.session.commit()
        print("Routes seeded successfully!")
    except Exception as e:
        print(f"Error seeding routes: {e}")

def seed_reviews():
    try:
        reviews = [
            Review(title="Great place!", content='I had a wonderful time here.', rating=4.7, image='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQJNs60im_OuCYbJQrjyrCRQ8i9saQ8514pSHSmv4OXOqvzkG7IITUwEiHSye2NBxhSHEE&usqp=CAU', place_id=1, user_id=1, created_at=datetime.utcnow()),
            Review(title="Amazing experience!", content='It was amazing people and culture.', image='https://www.itzcaribbean.com/wp-content/uploads/2014/05/black-cultural-archives-1.jpg', rating=4.5, place_id=2, user_id=2, created_at=datetime.utcnow()),
            Review(title="A must-visit!", content='Highly recommend this spot.', rating=4, image='https://www.kayak.com/rimg/himg/a2/f2/84/expediav2-1968-c61f3d-458091.jpg?width=968&height=607&crop=true', place_id=3, user_id=3, created_at=datetime.utcnow()),
            Review(title="Wonderful Experience!", content='The ambiance and service were exceptional.', rating=5.0, image='', place_id=14, user_id=20, likes=10, created_at=datetime.utcnow()),
            Review(title="Absolutely Fantastic!", content='A perfect place for a relaxing getaway.', rating=4.8, image='', place_id=15, user_id=21, likes=7, created_at=datetime.utcnow()),
            Review(title="Exceptional Service!", content='The staff went above and beyond to make our stay enjoyable.', rating=4.9, image='client/public/Review/pexels-apasaric-1134166.jpg', place_id=4, user_id=3, created_at=datetime.utcnow()),
            Review(title="Great Atmosphere!", content='Perfect spot for an evening out with friends.', rating=4.7, image='client/public/Review/pexels-ekrulila-8147953.jpg', place_id=4, user_id=4, created_at=datetime.utcnow()),
            Review(title="Highly Recommended!", content='An unforgettable experience with great food and ambiance.', rating=4.8, image='', place_id=5, user_id=5, created_at=datetime.utcnow()),
            Review(title="Perfect Location!", content='Great place with stunning views and fantastic service.', rating=5.0, image='', place_id=6, user_id=6, created_at=datetime.utcnow()),
            Review(title="Great Place to Relax!", content='Wonderful spot to unwind with excellent amenities.', rating=4.6, image='', place_id=7, user_id=7, created_at=datetime.utcnow()),
            Review(title="Amazing Experience!", content='Everything was perfect from start to finish.', rating=4.9, image='', place_id=8, user_id=8, created_at=datetime.utcnow()),
            Review(title="Fantastic Venue!", content='Great atmosphere with friendly staff and delicious food.', rating=4.8, image='', place_id=9, user_id=9, created_at=datetime.utcnow()),
            Review(title="Wonderful Place!", content='Highly recommend this spot for a great experience.', rating=4.7, image='', place_id=10, user_id=10, created_at=datetime.utcnow()),
            Review(title="Excellent Service!", content='Fantastic experience with amazing staff and facilities.', rating=5.0, image='', place_id=11, user_id=11, created_at=datetime.utcnow()),
            Review(title="Beautiful Location!", content='A great spot with beautiful scenery and top-notch amenities.', rating=4.9, image='', place_id=12, user_id=12, created_at=datetime.utcnow()),
            Review(title="Amazing Ambiance!", content='Loved the atmosphere and the attention to detail.', rating=4.8, image='', place_id=13, user_id=13, created_at=datetime.utcnow()),
            Review(title="Top-notch Experience!", content='Exceptional service and great facilities.', rating=4.9, image='', place_id=14, user_id=14, created_at=datetime.utcnow()),
            Review(title="Perfect for Relaxation!", content='A fantastic place to unwind and recharge.', rating=4.7, image='client/public/Review/pexels-efrem-efre-2786187-17655313.jpg', place_id=3, user_id=15, created_at=datetime.utcnow()),
            Review(title="Fantastic Food!", content='Delicious dishes and excellent service.', rating=4.8, image='', place_id=11, user_id=21, likes=7, created_at=datetime.utcnow()),
            Review(title="Wonderful Venue!", content='Great place with fantastic ambiance and service.', rating=4.9, image='client/public/Review/pexels-builtbyking-11403821.jpg', place_id=1, user_id=17, created_at=datetime.utcnow())
        ]
        db.session.bulk_save_objects(reviews)
        db.session.commit()
        print("Reviews seeded successfully!")
    except Exception as e:
        print(f"Error seeding reviews: {e}")

def seed_safety_marks():
    try:
        safety_marks = [
            SafetyMark(is_safe=True, place_id=1, user_id=1, created_at=datetime.utcnow()),
            SafetyMark(is_safe=False, place_id=2, user_id=2, created_at=datetime.utcnow()),
            SafetyMark(is_safe=True, place_id=3, user_id=3, created_at=datetime.utcnow()),
            SafetyMark(is_safe=True, place_id=4, user_id=7, created_at=datetime.utcnow()),
            SafetyMark(is_safe=False, place_id=5, user_id=8, created_at=datetime.utcnow()),
            SafetyMark(is_safe=True, place_id=6, user_id=13, created_at=datetime.utcnow()),
            SafetyMark(is_safe=True, place_id=7, user_id=10, created_at=datetime.utcnow()),
            SafetyMark(is_safe=False, place_id=8, user_id=12, created_at=datetime.utcnow()),
            SafetyMark(is_safe=True, place_id=9, user_id=13, created_at=datetime.utcnow()),
            SafetyMark(is_safe=True, place_id=10, user_id=11, created_at=datetime.utcnow()),
            SafetyMark(is_safe=False, place_id=12, user_id=21, created_at=datetime.utcnow()),
            SafetyMark(is_safe=True, place_id=13, user_id=16, created_at=datetime.utcnow()),
            SafetyMark(is_safe=True, place_id=11, user_id=17, created_at=datetime.utcnow()),
            SafetyMark(is_safe=False, place_id=14, user_id=14, created_at=datetime.utcnow()),
            SafetyMark(is_safe=True, place_id=15, user_id=4, created_at=datetime.utcnow())
        ]
        db.session.bulk_save_objects(safety_marks)
        db.session.commit()
        print("Safety marks seeded successfully!")
    except Exception as e:
        print(f"Error seeding safety marks: {e}")

def seed_comments():
    try:
        review1 = Review.query.filter_by(title="Great place!").first() 
        review2 = Review.query.filter_by(title="Amazing experience!").first() 
        review3 = Review.query.filter_by(title="A must-visit!").first() 
        review4 = Review.query.filter_by(title="Wonderful Experience!").first() 
        review5 = Review.query.filter_by(title="Absolutely Fantastic!").first() 
        review6 = Review.query.filter_by(title="Exceptional Service").first() 
        review7 = Review.query.filter_by(title="Great Atmosphere!").first() 
        review8 = Review.query.filter_by(title="Highly Recommended!").first() 
        
        review9 = Review.query.filter_by(title="Perfect Location!").first() 
        review10 = Review.query.filter_by(title="Great Place to Relax!").first() 
        review11 = Review.query.filter_by(title="Amazing Experience!").first() 
        review12 = Review.query.filter_by(title="Fantastic Venue!").first() 
        review13 = Review.query.filter_by(title="Wonderful Place!").first() 
        review14 = Review.query.filter_by(title="Excellent Service!").first()
        
        review15 = Review.query.filter_by(title="Beautiful Location!").first() 
        review16 = Review.query.filter_by(title="Amazing Ambiance!").first() 
        review17 = Review.query.filter_by(title="Top-notch Experience!").first() 
        review18 = Review.query.filter_by(title="Perfect for Relaxation!").first() 
        review19 = Review.query.filter_by(title="Fantastic Food!").first() 
        review20 = Review.query.filter_by(title="Wonderful Venue!").first()

        comments = [
            Comment(content="I'm planning a trip there now love this!", user_id=1, review=review1),
            Comment(content="What was your favorite part?", user_id=2, review=review16),
            Comment(content="What was the food like?", user_id=3, review=review20),
            Comment(content ="I cant wait to go!", user_id=6, review=review12),
            Comment(content="I went last year and it was amazing!", user_id=8, review=review10),
            Comment(content="Can you recommend places for me?", user_id=12, review=review4),
            Comment(content="I love this!", user_id=16, review=review17),
            Comment(content="Thanks for sharing", user_id=7, review=review10),
            Comment(content="Can't wait to go!", user_id=19, review=review11),
            Comment(content="This is lovely!", user_id=21, review=review12),
            Comment(content="On my togo list", user_id=5, review=review8),
            Comment(content ="I would love to go!", user_id=13, review=review18)
        ]
        db.session.add(comments)
        db.session.commit()

        print("Comments seeded successfully!")
    except Exception as e:
        print(f"Error seeding Comments: {e}")

def seed_likes():
    try:
        review1 = Review.query.filter_by(title="Great place!").first() 
        review2 = Review.query.filter_by(title="Amazing experience!").first() 
        review3 = Review.query.filter_by(title="A must-visit!").first() 
        review4 = Review.query.filter_by(title="Wonderful Experience!").first() 
        review5 = Review.query.filter_by(title="Absolutely Fantastic!").first() 
        review6 = Review.query.filter_by(title="Exceptional Service").first() 
        review7 = Review.query.filter_by(title="Great Atmosphere!").first() 
        review8 = Review.query.filter_by(title="Highly Recommended!").first() 
        
        review9 = Review.query.filter_by(title="Perfect Location!").first() 
        review10 = Review.query.filter_by(title="Great Place to Relax!").first() 
        review11 = Review.query.filter_by(title="Amazing Experience!").first() 
        review12 = Review.query.filter_by(title="Fantastic Venue!").first() 
        review13 = Review.query.filter_by(title="Wonderful Place!").first() 
        review14 = Review.query.filter_by(title="Excellent Service!").first()
        
        review15 = Review.query.filter_by(title="Beautiful Location!").first() 
        review16 = Review.query.filter_by(title="Amazing Ambiance!").first() 
        review17 = Review.query.filter_by(title="Top-notch Experience!").first() 
        review18 = Review.query.filter_by(title="Perfect for Relaxation!").first() 
        review19 = Review.query.filter_by(title="Fantastic Food!").first() 
        review20 = Review.query.filter_by(title="Wonderful Venue!").first()
   
        likes = [   
            Like(user_id=[1,4,7,5,8,13,21], review=review20),
            Like(user_id=[1,14,16.7,3,4,6,2,8], review=review3),
            Like(user_id=[11,15,18,3,2,4,6,7,9,19], review=review1),
            Like(user_id=[13,7,4,2,1,8,9,11], review=review2),
            Like(user_id=[15,7,4,2,3,9], review=review4),
            Like(user_id=[16,17,19,21,20], review=review5),
            Like(user_id=[1,21,5,7,19,18], review=review6),
            Like(user_id=[18,20,19,18,14,3], review=review7),
            Like(user_id=[11,2], review=review8),
            Like(user_id=[1,7,18,19,21], review=review9),
            Like(user_id=[14,6,4,18,19,20], review=review10),
            Like(user_id=[1,9,19,16,15,6,3], review=review14),
            Like(user_id=[19,13,12,7,5,3], review=review13),
            Like(user_id=[15,7,9,10,4,14], review=review11),
            Like(user_id=[14,10,19,16,5], review=review12),
            Like(user_id=[12,11,14,2,9], review=review15),
            Like(user_id=[17,8,4,10,11], review=review17),
            Like(user_id=[11,7,6,3,9,14], review=review16),
            Like(user_id=[10,9,8,4,6,18], review=review18),
            Like(user_id=[1,16,18,21,19], review=review19)
        ]  

        db.session.add(likes)
        db.session.commit()

        print("Likes seeded successfully!")
    except Exception as e:
        print(f"Error seeding Likes: {e}") 

def seed_messages():
    messages = [
        Message(content='Hello, how are you?', user_id=1, conversation_id=1),
        Message(content='I am good, thanks!', user_id=2, conversation_id=1),
        Message(content='Are you coming to the event?', user_id=3, conversation_id=2),
        Message(content='What time is it', user_id=4, conversation_id=2),
    ]

# Adding the data to the table
    db.session.add_all(messages)
    db.session.commit()

def seed_conversations():
    conversations = [
        Conversation(user1_id=1, user2_id=2),
        Conversation(user1_id=1, user2_id=3),
    ]

    # Adding the data to the table
    db.session.add_all(conversations)
    db.session.commit()

def seed_notifications():
    notifications = [
        Notification(content='You have a new message', user_id=1),
        Notification(content='Your review got a like', user_id=2),
    ]

    # Adding the data to the table
    db.session.add_all(notifications)
    db.session.commit()

def seed_history():
    history = [
        History(action='User logged in', user_id=1),
        History(action='User updated profile', user_id=2),
    ]

    # Adding the data to the table
    db.session.add_all(history)
    db.session.commit()

def seed_follows():
    follows = [
        Follow(follower_id=1, following_id=2),
        Follow(follower_id=2, following_id=3),
    ]

    # Adding the data to the table
    db.session.add_all(follows)
    db.session.commit()

def seed_followers():
    followers = [
        Follower(user_id=2),
        Follower(user_id=3),
        Follower(user_id=2),
        Follower(user_id=3),
        Follower(user_id=2),
        Follower(user_id=3),
    ]
    db.session.add_all(followers)
    db.session.commit()

def seed_followings():
    followings = [
        Following(user_id=1),
        Following(user_id=2),
        Following(user_id=1),
        Following(user_id=2),
        Following(user_id=1),
        Following(user_id=2),
        Following(user_id=1),
        Following(user_id=2),
    ]

    db.session.add_all(followings)
    db.session.commit()

def seed_stories():
    stories = [
        Story(media='https://www.youtube.com/shorts/EBDrxKcyTFk?feature=share', user_id=1),
        Story(media='https://www.youtube.com/shorts/gbrE9RqQimE?feature=share', user_id=2),
    ]

    # Adding the data to the table
    db.session.add_all(stories)
    db.session.commit()


def recreate_and_seed_db():
    try:
        with app.app_context():
            db.drop_all()
            db.create_all()
            seed_users()
            seed_places()
            seed_routes()
            seed_reviews()
            seed_likes()
            seed_safety_marks()
            seed_messages()
            seed_conversations()
            seed_notifications()
            seed_history()
            seed_follows()
            seed_followers()
            seed_followings()
            seed_stories()
            print("Database recreated and seeded successfully!")
    except Exception as e:
        print(f"Error recreating and seeding the database: {e}")

if __name__ == '__main__':
    recreate_and_seed_db()
