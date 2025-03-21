from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models import City


class CityRepository:
    @staticmethod
    def create_city(db: Session, city_data: dict):
        """Creates a new city if it does not exist."""
        existing_city = db.query(City).filter(City.name == city_data["name"]).first()
        if existing_city:
            return None  # Avoid duplicate city names
        city = City(**city_data)
        db.add(city)
        try:
            db.commit()
            db.refresh(city)
            return city
        except IntegrityError:
            db.rollback()
            return None  # Handle duplicate entry error

    @staticmethod
    def get_all_cities(db: Session):
        """Retrieves all registered cities."""
        return db.query(City).all()

    @staticmethod
    def get_city_by_id(db: Session, city_id: int):
        """Fetches a city by its ID."""
        return db.query(City).filter(City.id == city_id).first()

    @staticmethod
    def update_city(db: Session, city_id: int, updated_data: dict):
        """Updates a city's details (name/state)."""
        city = db.query(City).filter(City.id == city_id).first()
        if city:
            for key, value in updated_data.items():
                setattr(city, key, value)
            db.commit()
            db.refresh(city)
        return city

    @staticmethod
    def delete_city(db: Session, city_id: int):
        """Deletes a city by ID."""
        city = db.query(City).filter(City.id == city_id).first()
        if city:
            db.delete(city)
            db.commit()
            return True
        return False
