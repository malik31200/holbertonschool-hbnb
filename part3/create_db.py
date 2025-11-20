from app import create_app, db
from app.services.facade import facade

app = create_app()

with app.app_context():
    # Création des tables
    db.create_all()
    print("Tables créées ✅")

    # Création user test si besoin
    user = facade.get_user_by_email("test@example.com")
    if not user:
        user = facade.create_user({
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "password": "1234",
            "is_admin": False
        })
        print("User test créé : test@example.com / 1234")

    print("\n--- Création de places de test ---")

    places_to_create = [
        {
            "title": "Studio Paris Centre",
            "description": "Studio cosy proche de tout.",
            "price": 80.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": user.id,
            "rooms": 1,
            "capacity": 2,
            "surface": 25.0
        },
        {
            "title": "Maison Toulouse Sud",
            "description": "Grande maison familiale.",
            "price": 120.0,
            "latitude": 43.6045,
            "longitude": 1.4442,
            "owner_id": user.id,
            "rooms": 4,
            "capacity": 6,
            "surface": 120.0
        },
        {
            "title": "Appartement Lyon Confluence",
            "description": "Appartement moderne dans un quartier dynamique.",
            "price": 95.0,
            "latitude": 45.7485,
            "longitude": 4.8467,
            "owner_id": user.id,
            "rooms": 3,
            "capacity": 5,
            "surface": 75.0
        },
        {
            "title": "Loft Marseille Vieux Port",
            "description": "Loft lumineux avec vue port.",
            "price": 150.0,
            "latitude": 43.2965,
            "longitude": 5.3698,
            "owner_id": user.id,
            "rooms": 2,
            "capacity": 4,
            "surface": 55.0
        },
        {
            "title": "Chalet Grenoble Montagne",
            "description": "Chalet rustique idéal ski.",
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

    for place_data in places_to_create:
        if place_data["title"] not in existing_titles:
            place = facade.create_place(place_data)
            print(f"Place créée : {place.title}")
        else:
            print(f"Place déjà existante : {place_data['title']}")

    print("✔ Création des places terminée")
