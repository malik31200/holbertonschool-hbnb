#!/usr/bin/env python3
from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    user = User.query.filter_by(email="test@example.com").first()
    if user:
        db.session.delete(user)
        db.session.commit()
        print("Utilisateur supprimé")
    else:
        print("Utilisateur non trouvé")
