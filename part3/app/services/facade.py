from app.persistence.sqlalchemy_repository import SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    """Facade class to manage users, places, reviews, and amenities."""
    def __init__(self):
        """
        Facade constructor to initialize repositories for
        users, places, reviews, and amenities.
        """

        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    # ---------- User ---------- #

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Retrieve all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        """Update a user’s information."""
        user = self.user_repo.get(user_id)
        if not user:
            return None

        try:
            updated_user = self.user_repo.update(user_id, data)
            return updated_user
        except ValueError as e:
            raise e

    # ---------- Amenity ---------- #

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def get_amenity_by_name(self, name: str):
        if hasattr(self.amenity_repo, "get_by_attribute"):
            return self.amenity_repo.get_by_attribute("name", name)
        for obj in self.amenity_repo.get_all():
            if getattr(obj, "name", None) == name:
                return obj
        return None

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        for key, value in amenity_data.items():
            setattr(amenity, key, value)
        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity

    # ---------- Place ---------- #

    def create_place(self, place_data):
        owner_id = place_data.get('owner_id')
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Owner is not found")

        amenity_ids = place_data.pop('amenities', [])

        place = Place(**place_data)

        for a_id in amenity_ids:
            amenity = self.amenity_repo.get(a_id)
            if amenity:
                place.amenities.append(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        for key, value in place_data.items():
            if key == 'amenities':
                new_amenities = []
                for amenity_id in value:
                    amenity = self.amenity_repo.get(amenity_id)
                    if amenity:
                        new_amenities.append(amenity)
                place.amenities = new_amenities
            elif hasattr(place, key):
                setattr(place, key, value)

        self.place_repo.update(place_id, place_data)
        return place

    # ---------- Reviews ---------- #

    def create_review(self, review_data):
        user = self.user_repo.get(review_data.get('user_id'))
        if not user:
            raise ValueError("Place not found")

        place = self.place_repo.get(review_data.get('place_id'))
        if not place:
            raise ValueError("Place not found")

        review = Review(
            text=review_data.get('text'),
            rating=review_data.get('rating'),
            user=user,
            place=place
            
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        reviews = []
        for r in self.review_repo.get_all():
            if r.place.id == place_id:
                reviews.append(r)
        return reviews

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        if 'text' in review_data:
            review.text = review_data['text']
        if 'rating' in review_data:
            rating = review_data['rating']
            if not (1 <= rating <= 5):
                raise ValueError("Rating must be between 1 and 5")
            review.rating = rating

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.delete(review_id)
        return review


facade = HBnBFacade()
