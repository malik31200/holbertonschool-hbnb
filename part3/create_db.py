from app import create_app, db
from app.services.facade import facade
from app.models import User

app = create_app()

with app.app_context():
    # Create tables
    db.create_all()
    print("Tables created ✅\n")

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

    print("--- Creating test places ---\n")

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
            "surface": 25.0
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
            "surface": 120.0
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
            "surface": 75.0
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
            "surface": 55.0
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
            "surface": 140.0
        }
    ]

    existing_titles = {p.title for p in facade.get_all_places()}
    created_places = []

    for place_data in places_to_create:
        if place_data["title"] not in existing_titles:
            place = facade.create_place(place_data)
            created_places.append(place)
            print(f"Place created: {place.title}")
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

    print("\n✔ Database setup complete!")
