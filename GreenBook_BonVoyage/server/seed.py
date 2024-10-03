from datetime import datetime
from config import bcrypt
from app import app, db
from models import User, Place, Conversation, Follow, History, Notification, Review, Route, SafetyMark, Story, Comment, Message, Like
# Filling the database with users
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
# Filling the database with places
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
# Filling the database with routes
def seed_routes():
    try:
# Letting the system know the places we put in the database
        places = {
            "Kwame Nkrumah Memorial Park & Mausoleum": Place.query.filter_by(name='Kwame Nkrumah Memorial Park & Mausoleum').first(),
            "Black Cultural Archives": Place.query.filter_by(name='Black Cultural Archives').first(),
            'La Chèvre d’Or': Place.query.filter_by(name='La Chèvre d’Or').first(),
            'teamLab Borderless: MORI Building DIGITAL ART MUSEUM': Place.query.filter_by(name='teamLab Borderless: MORI Building DIGITAL ART MUSEUM').first(),
            'Moses Mabhida Stadium': Place.query.filter_by(name='Moses Mabhida Stadium').first(),
            'Everland': Place.query.filter_by(name='Everland').first(),
            'Iguazu Falls': Place.query.filter_by(name='Iguazu Falls').first(),
            'Market Square Park': Place.query.filter_by(name='Market Square Park').first(),
            'Georgia Aquarium': Place.query.filter_by(name='Georgia Aquarium').first(),
            'Times Square': Place.query.filter_by(name='Times Square').first(),
            'Anza-Borrego Desert State Park': Place.query.filter_by(name='Anza-Borrego Desert State Park').first(),
            '27 Waterfalls of Damajagua': Place.query.filter_by(name='27 Waterfalls of Damajagua').first(),
            'Blue Hole Mineral Spring': Place.query.filter_by(name='Blue Hole Mineral Spring').first(),
            'Martha Brae River': Place.query.filter_by(name='Martha Brae River').first(),
            'Trafalgar Square': Place.query.filter_by(name='Trafalgar Square').first(),
        }
# Filling in our routes according to the places
        routes = [
            Route(name="Tour of Accra", user_id=1, places=[places['Kwame Nkrumah Memorial Park & Mausoleum'], places['Moses Mabhida Stadium']]),
            Route(name="London Highlights", user_id=2, places=[places['Black Cultural Archives'], places['La Chèvre d’Or']]),
            Route(name="Eze's Wonders", user_id=3, places=[places['Black Cultural Archives'], places['Trafalgar Square']]),
            Route(name="Tour of Accra", user_id=6, places=[places['Times Square'], places['Georgia Aquarium']]),
            Route(name="London Highlights", user_id=8, places=[places['Times Square'], places['Anza-Borrego Desert State Park']]),
            Route(name="Eze's Wonders", user_id=12, places=[places['Georgia Aquarium'],places['Market Square Park']]),
            Route(name="Tour of Accra", user_id=1, places=[places['27 Waterfalls of Damajagua'], places['Iguazu Falls']]),
            Route(name="London Highlights", user_id=7, places=[places['Blue Hole Mineral Spring'], places['Martha Brae River']]),
            Route(name="Eze's Wonders", user_id=16, places=[places['27 Waterfalls of Damajagua'], places['Martha Brae River']]),
            Route(name="Tour of Accra", user_id=21, places=[places['teamLab Borderless: MORI Building DIGITAL ART MUSEUM'], places['Everland']]),
            Route(name="London Highlights", user_id=2, places=[places['Iguazu Falls'], places['Market Square Park']]),
            Route(name="Eze's Wonders", user_id=3, places=[places['Georgia Aquarium'], places['Anza-Borrego Desert State Park']])
        ]
        db.session.bulk_save_objects(routes)
        db.session.commit()
        print("Routes seeded successfully!")
    except Exception as e:
        print(f"Error seeding routes: {e}")
# Filling the database with reviews
def seed_reviews():
    try:
        reviews = [
            Review(title="Great place!", content='I had a wonderful time here.', rating=4.7, image='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQJNs60im_OuCYbJQrjyrCRQ8i9saQ8514pSHSmv4OXOqvzkG7IITUwEiHSye2NBxhSHEE&usqp=CAU', place_id=1, user_id=1, created_at=datetime.utcnow()),
            Review(title="Amazing experience!", content='It was amazing people and culture.', image='https://www.itzcaribbean.com/wp-content/uploads/2014/05/black-cultural-archives-1.jpg', rating=4.5, place_id=2, user_id=2, created_at=datetime.utcnow()),
            Review(title="A must-visit!", content='Highly recommend this spot.', rating=4, image='https://www.kayak.com/rimg/himg/a2/f2/84/expediav2-1968-c61f3d-458091.jpg?width=968&height=607&crop=true', place_id=3, user_id=3, created_at=datetime.utcnow()),
            Review(title="Wonderful Experience!", content='The ambiance and service were exceptional.', rating=5.0, place_id=14, user_id=20, created_at=datetime.utcnow()),
            Review(title="Absolutely Fantastic!", content='A perfect place for a relaxing getaway.', rating=4.8, place_id=15, user_id=21, created_at=datetime.utcnow()),
            Review(title="Exceptional Service!", content='The staff went above and beyond to make our stay enjoyable.', rating=4.9, image='client/public/Review/pexels-apasaric-1134166.jpg', place_id=4, user_id=3, created_at=datetime.utcnow()),
            Review(title="Great Atmosphere!", content='Perfect spot for an evening out with friends.', rating=4.7, image='client/public/Review/pexels-ekrulila-8147953.jpg', place_id=4, user_id=4, created_at=datetime.utcnow()),
            Review(title="Highly Recommended!", content='An unforgettable experience with great food and ambiance.', rating=4.8, place_id=5, user_id=5, created_at=datetime.utcnow()),
            Review(title="Perfect Location!", content='Great place with stunning views and fantastic service.', rating=5.0, place_id=6, user_id=6, created_at=datetime.utcnow()),
            Review(title="Great Place to Relax!", content='Wonderful spot to unwind with excellent amenities.', rating=4.6, place_id=7, user_id=7, created_at=datetime.utcnow()),
            Review(title="Amazing Experience!", content='Everything was perfect from start to finish.', rating=4.9, place_id=8, user_id=8, created_at=datetime.utcnow()),
            Review(title="Fantastic Venue!", content='Great atmosphere with friendly staff and delicious food.', rating=4.8, place_id=9, user_id=9, created_at=datetime.utcnow()),
            Review(title="Wonderful Place!", content='Highly recommend this spot for a great experience.', rating=4.7, place_id=10, user_id=10, created_at=datetime.utcnow()),
            Review(title="Excellent Service!", content='Fantastic experience with amazing staff and facilities.', rating=5.0, place_id=11, user_id=11, created_at=datetime.utcnow()),
            Review(title="Beautiful Location!", content='A great spot with beautiful scenery and top-notch amenities.', rating=4.9, place_id=12, user_id=12, created_at=datetime.utcnow()),
            Review(title="Amazing Ambiance!", content='Loved the atmosphere and the attention to detail.', rating=4.8, place_id=13, user_id=13, created_at=datetime.utcnow()),
            Review(title="Top-notch Experience!", content='Exceptional service and great facilities.', rating=4.9, place_id=14, user_id=14, created_at=datetime.utcnow()),
            Review(title="Perfect for Relaxation!", content='A fantastic place to unwind and recharge.', rating=4.7, image='client/public/Review/pexels-efrem-efre-2786187-17655313.jpg', place_id=3, user_id=15, created_at=datetime.utcnow()),
            Review(title="Fantastic Food!", content='Delicious dishes and excellent service.', rating=4.8, place_id=11, user_id=21, created_at=datetime.utcnow()),
            Review(title="Wonderful Venue!", content='Great place with fantastic ambiance and service.', rating=4.9, image='client/public/Review/pexels-builtbyking-11403821.jpg', place_id=1, user_id=17, created_at=datetime.utcnow())
        ]
        db.session.bulk_save_objects(reviews)
        db.session.commit()
        print("Reviews seeded successfully!")
    except Exception as e:
        print(f"Error seeding reviews: {e}")
# Filling the database with safety marks
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
# Filling the database with comments
def seed_comments():
    try:
# Reminding the system of the reviews we set
        review_ids = {
            "Great place!": 1, "Amazing experience!": 2, "A must-visit!": 3, "Wonderful Experience!":4, "Absolutely Fantastic!":5,
            "Exceptional Service":6, "Great Atmosphere!":7, "Highly Recommended!":8, "Perfect Location!":9,
            "Great Place to Relax!":10, "Amazing Experience!":11, "Fantastic Venue!":12, "Wonderful Place!":13,
            "Excellent Service!":14, "Beautiful Location!":15, "Amazing Ambiance!":16, "Top-notch Experience!":17, "Perfect for Relaxation!":18,
            "Fantastic Food!":19, "Wonderful Venue!":20,
        }
        reviews = {title: db.session.get(Review, review_ids[title]) for title in review_ids.keys()}
# Filling in the comments acording to the reviews
        comments = [
        
            Comment(content="I'm planning a trip there now love this!", user_id=1, review_id=1),
            Comment(content="What was your favorite part?", user_id=2, review_id=2),
            Comment(content="What was the food like?", user_id=3, review_id=4),
            Comment(content ="I cant wait to go!", user_id=6, review_id=12),
            Comment(content="I went last year and it was amazing!", user_id=8, review_id=10),
            Comment(content="Can you recommend places for me?", user_id=12, review_id=4),
            Comment(content="I love this!", user_id=16, review_id=17),
            Comment(content="Thanks for sharing", user_id=7, review_id=10),
            Comment(content="Can't wait to go!", user_id=19, review_id=11),
            Comment(content="This is lovely!", user_id=21, review_id=12),
            Comment(content="On my togo list", user_id=5, review_id=8),
            Comment(content ="I would love to go!", user_id=13, review_id=18)
        ]
  
        db.session.add_all(comments)
        db.session.commit()

        print("Comments seeded successfully!")
    except Exception as e:
        print(f"Error seeding Comments: {e}")
# Filling the database with likes
def seed_likes():
    try:
        review_ids = {
            "Great place!": 1, "Amazing experience!": 2, "A must-visit!": 3, "Wonderful Experience!":4, "Absolutely Fantastic!":5,
            "Exceptional Service":6, "Great Atmosphere!":7, "Highly Recommended!":8, "Perfect Location!":9,
            "Great Place to Relax!":10, "Amazing Experience!":11, "Fantastic Venue!":12, "Wonderful Place!":13,
            "Excellent Service!":14, "Beautiful Location!":15, "Amazing Ambiance!":16, "Top-notch Experience!":17, "Perfect for Relaxation!":18,
            "Fantastic Food!":19, "Wonderful Venue!":20,
        }
        reviews = {title: db.session.get(Review, review_ids[title]) for title in review_ids.keys()}

      
        likes = [
            Like(user_id=user_id, review_id=review_id, liked_at=datetime.utcnow())
            for user_id, review_id in [
                (1, 1), (2, 2), (3, 1), (4, 3)  # Make sure these review_id values exist
            ]
        ]
    

        db.session.add_all(likes)
        db.session.commit()

        print("Likes seeded successfully!")
    except Exception as e:
        print(f"Error seeding Likes: {e}") 
# Filling the database with messages
def seed_messages():
    try:
        messages = [
# Make sure sender_id and recipient_id are correctly matched
            Message(content='Hello, how are you?', sender_id=1, recipient_id=2, conversation_id=1),
            Message(content='I am good, thanks!', sender_id=2, recipient_id=1, conversation_id=1),
            Message(content='Are you coming to the event?', sender_id=3, recipient_id=4, conversation_id=2),
            Message(content='What time is it?', sender_id=4, recipient_id=3, conversation_id=2),
        ]

# Adding the data to the table
        db.session.add_all(messages)
        db.session.commit()

        print("Messages seeded successfully!")
    except Exception as e:
        print(f"Error seeding Messages: {e}")

# Filling the database with conversations
def seed_conversations():
    try:
        conversations = [
# Ensure that sender_id and recipient_id are valid user IDs
            Conversation(sender_id=1, recipient_id=2),
            Conversation(sender_id=1, recipient_id=3),
        ]

# Adding the data to the table
        db.session.add_all(conversations)
        db.session.commit()
        print("Conversations seeded successfully!")
    except Exception as e:
        print(f"Error seeding Conversations: {e}")
# Filling the database with notifcations
def seed_notifications():
    try:
        notifications = [
            Notification(message='You have a new message', user_id=1),
            Notification(message='Your review got a like', user_id=2),
        ]

# Adding the data to the table
        db.session.add_all(notifications)
        db.session.commit()
        print("Notfication seeded successfully!")
    except Exception as e:
        print(f"Error seeding Notification: {e}") 
# Filling the database with history
def seed_history():
    try:
        history = [
            History(action='User logged in', user_id=1),
            History(action='User updated profile', user_id=2),
        ]

# Adding the data to the table
        db.session.add_all(history)
        db.session.commit()
        print("History seeded successfully!")
    except Exception as e:
        print(f"Error seeding History: {e}") 
#filling the database with follows
def seed_follows():
    try:
        follow_data = {
            2: [1, 16, 18, 21, 19],
            1: [16, 2, 21, 19],
            3: [11, 6, 8, 21, 19],
            4: [17, 7, 5, 21, 18],
            5: [10, 16, 8, 1, 18],
            6: [12, 16, 11, 2, 9],
            7: [1, 6, 18, 21, 19],
            8: [13, 7, 5, 12, 20],
            9: [1, 3, 9, 11, 12],
            10: [15, 14, 17, 12, 19],
            11: [19, 8, 15, 20, 13, 11]
        }

# Retrieve users
        users = User.query.filter(User.id.in_(follow_data.keys())).all()
        user_dict = {user.id: user for user in users}

# Add follows
        for user_id, follow_ids in follow_data.items():
            user = user_dict.get(user_id)
            if user:
                for follow_id in follow_ids:
                    followed_user = user_dict.get(follow_id)
                    if followed_user:
                        user.following.append(followed_user)

        db.session.commit()
        print("Follows seeded successfully!")
    except Exception as e:
        print(f"Error seeding Follows: {e}") 

# Filling the database with stories
def seed_stories():
    try:
        stories = [
            Story(media='https://www.youtube.com/shorts/EBDrxKcyTFk?feature=share', user_id=11),
            Story(media='https://www.youtube.com/shorts/gbrE9RqQimE?feature=share', user_id=21),
            Story(media='client/public/Stories/dumbuggy.mp4', user_id=14),
            Story(media='client/public/Stories/asia2.mp4', user_id=2),
            Story(media='client/public/Stories/man.mp4', user_id=7),
            Story(media='client/public/Stories/asia.mp4', user_id=8),
        ]

        
        db.session.add_all(stories)
        db.session.commit()
        print("Likes seeded successfully!")
    except Exception as e:
        print(f"Error seeding Likes: {e}") 


def recreate_and_seed_db():
    try:
        with app.app_context():
            db.drop_all()
            db.create_all()

# Seed each table
            seed_users()
            seed_places()
            seed_routes()
            seed_reviews()
            seed_safety_marks()
            seed_comments()
            seed_likes()
            seed_messages()
            seed_conversations()
            seed_notifications()
            seed_history()
            seed_follows()
            # seed_followers()
            # seed_followings()
            seed_stories()
            print("Database recreated and seeded successfully!")
    except Exception as e:
        print(f"Error recreating and seeding the database: {e}")

if __name__ == '__main__':
    recreate_and_seed_db()
# Look at app.db