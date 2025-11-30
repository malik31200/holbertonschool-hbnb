from app import create_app, db
from app.services.facade import facade
from app.models import User
import os

app = create_app()

IMAGES_FOLDER = '/home/malik31200/holbertonschool-hbnb/part4/base_files/images'

with app.app_context():
    # Create tables
    db.create_all()
    print("Tables created \n")

    # Create test user if not exists
    user = facade.get_user_by_email("test@example.com")
    if not user:
        user = facade.create_user({
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "1234",
            "is_admin": False
        })
        print("Test user created: test@example.com / 1234\n")

    print("--- Looking for images ---\n")
    available_images = []
    
    if os.path.exists(IMAGES_FOLDER):
        available_images = [f for f in os.listdir(IMAGES_FOLDER)
                            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp'))]
        print(f"Found {len(available_images)} images: {available_images}\n")
        available_images.sort()
    else:
        print(f"⚠️  Warning: Images folder not found at {IMAGES_FOLDER}")

    print(f"Found {len(available_images)} images: {available_images}\n")

    places_to_create = [
        {
            "title": "Paris Center Studio",
            "description": "Cozy studio in the heart of Paris.",
            "price": 80.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": user.id,
            "rooms": 1,
            "capacity": 2,
            "surface": 25.0,
            "photos": [f"/images/{available_images[0]}"] if len(available_images) > 0 else []
        },
        {
            "title": "Toulouse South House",
            "description": "Spacious family house in Toulouse.",
            "price": 120.0,
            "latitude": 43.6045,
            "longitude": 1.4442,
            "owner_id": user.id,
            "rooms": 4,
            "capacity": 6,
            "surface": 120.0,
            "photos": [f"/images/{available_images[1]}"] if len(available_images) > 1 else []
        },
        {
            "title": "Lyon Confluence Apartment",
            "description": "Modern apartment in a dynamic neighborhood.",
            "price": 95.0,
            "latitude": 45.7485,
            "longitude": 4.8467,
            "owner_id": user.id,
            "rooms": 3,
            "capacity": 5,
            "surface": 75.0,
            "photos": [f"/images/{available_images[2]}"] if len(available_images) > 2 else []
        },
        {
            "title": "Marseille Vieux Port Loft",
            "description": "Bright loft with port view.",
            "price": 150.0,
            "latitude": 43.2965,
            "longitude": 5.3698,
            "owner_id": user.id,
            "rooms": 2,
            "capacity": 4,
            "surface": 55.0,
            "photos": [f"/images/{available_images[3]}"] if len(available_images) > 3 else []
        },
        {
            "title": "Grenoble Mountain Chalet",
            "description": "Rustic chalet perfect for skiing.",
            "price": 200.0,
            "latitude": 45.1885,
            "longitude": 5.7245,
            "owner_id": user.id,
            "rooms": 5,
            "capacity": 8,
            "surface": 140.0,
            "photos": [f"/images/{available_images[4]}"] if len(available_images) > 4 else []
        }
    ]

    existing_titles = {p.title for p in facade.get_all_places()}
    created_places = []

    for place_data in places_to_create:
        if place_data["title"] not in existing_titles:
            place = facade.create_place(place_data)
            created_places.append(place)
            print(f"Place created: {place.title} with photos: {place.photos}")
        else:
            print(f"Place already exists: {place_data['title']}")

    print("\n--- Creating test reviews ---\n")

    for place in created_places:
        reviews_to_create = [
            {"user_id": user.id, "place_id": place.id, "rating": 5, "text": "Amazing stay! Highly recommended."},
            {"user_id": user.id, "place_id": place.id, "rating": 4, "text": "Very comfortable and clean."}
        ]
        for rev in reviews_to_create:
            facade.create_review(rev)
            print(f"Review added for {place.title}: {rev['text']}")

    print("\n Database setup complete!")
