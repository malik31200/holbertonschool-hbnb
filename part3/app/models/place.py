import uuid
from datetime import datetime
from app import db

place_amenity = db.Table(
    "place_amenity",
    db.Column("place_id", db.String(36), db.ForeignKey("places.id", ondelete="CASCADE"), primary_key=True),
    db.Column("amenity_id", db.String(36), db.ForeignKey("amenities.id", ondelete="CASCADE"), primary_key=True)
)

from sqlalchemy.orm import validates

class Place(db.Model):
    __tablename__ = "places"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Float, default=0.0)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    owner_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    reviews = db.relationship('Review', back_populates='place', cascade='all, delete-orphan')
    rooms = db.Column(db.Integer, default=1)
    capacity = db.Column(db.Integer, default=1)
    surface = db.Column(db.Float, default=0.0)
    description = db.Column(db.String(512), default="")
    photos = db.Column(db.JSON, default=list)

    owner = db.relationship("User", back_populates="places", lazy=True)

    amenities = db.relationship(
    "Amenity",
    secondary=place_amenity,
    back_populates="places",
    lazy="subquery"
)

    reviews = db.relationship(
    "Review",
    back_populates="place",
    cascade="all, delete-orphan"
)

    @validates('title')
    def validate_title(self, key, value):
        if not value or len(value) > 100:
            raise ValueError("Title required, max 100 chars")
        return value

    @validates('price')
    def validate_price(self, key, value):
        if value < 0:
            raise ValueError("Price must be positive")
        return value

    @validates('latitude')
    def validate_latitude(self, key, value):
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        return value

    @validates('longitude')
    def validate_longitude(self, key, value):
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 et 180")
        return value


    def add_review(self, review):
        """Add a review to the place."""
        if review not in self.reviews:
            self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def to_dict(self, include_related=False):
        """Return a JSON-serializable dictionary."""
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "photos": self.photos or [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

        if include_related:
            data["amenities"] = [a.to_dict() for a in self.amenities]
            data["reviews"] = [r.to_dict() for r in self.reviews]

        return data

    def __repr__(self):
        return f"<Place {self.title} (owner={self.owner_id})>"
