from app import create_app, db
from app.models.user import User
from app.services.facade import facade

app = create_app()

with app.app_context():
    # Données de l'utilisateur
    user_data = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "password": "password123",
        "is_admin": False
    }

    # Création via le facade
    user = facade.create_user(user_data)
    print("Utilisateur de test créé :", user.email, "/ password123")
