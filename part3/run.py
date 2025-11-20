from app import create_app
from app.services.facade import facade

app = create_app()

with app.app_context():
    if not facade.get_user_by_email("john.doe@example.com"):
        facade.create_user({
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "1234",
            "is_admin": False
        })
        print("User test create : john.doe@example.com / 1234")

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
